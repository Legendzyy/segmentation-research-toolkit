# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""ENG04: I0 GT-linked task transfer; X0 CrossKD head-input YOLO adaptation.

X0 preserves cross-head gradient, channel scale alignment, KD-QFL beta1,
and same-location DFL KL T1. YOLO TAL/positive-count normalization and
1x1 width adapters are explicit adaptations; mask remains native-supervised.
"""
import torch
import torch.nn.functional as F
from torch import nn
from ultralytics.nn.distill_model import DistillationModel
from .output_kd import elementwise_iou

class TransferModel(DistillationModel):
    def __init__(self, teacher_checkpoint, student_model, mode):
        assert mode in ('X0','I0','I1','J0')
        super().__init__(teacher_checkpoint,student_model)
        dims=[(self._student_feats[i].shape[1],self._teacher_feats[i].shape[1]) for i in (16,19,22)]
        self._remove_feature_hooks()
        self.feats_idx=[16,19,22] if mode=='X0' else []
        self.projector=nn.ModuleList([nn.Conv2d(s,t,1) for s,t in dims] if mode=='X0' else [])
        self._register_feature_hooks()
        self.mode=mode; self.kd_enabled=True; self.kd_scale=1.; self.last_audit={}
        self.teacher_model.args=student_model.args
        self._teacher_criterion=None
        self._freeze_teacher()

    @staticmethod
    def align_scale(s,t):
        dims=(0,2,3)
        return (s-s.mean(dims,keepdim=True))/(s.std(dims,keepdim=True)+1e-6)*t.std(dims,keepdim=True)+t.mean(dims,keepdim=True)

    def cross_loss(self,s,t,batch):
        if not len(batch['cls']):
            self.last_audit={'empty_GT_batch':True,'KD_skipped':True}
            return s['scores'].float().sum()*0
        head=self.teacher_model.model[-1]; bs=len(batch['img'])
        xs=[self.align_scale(p(self._student_feats[i].float()),self._teacher_feats[i].detach().float()) for i,p in zip(self.feats_idx,self.projector)]
        scores=torch.cat([head.cv3[i](x).view(bs,head.nc,-1) for i,x in enumerate(xs)],2)
        boxes=torch.cat([head.cv2[i](x).view(bs,4*head.reg_max,-1) for i,x in enumerate(xs)],2)
        with torch.no_grad():
            positives=self.student_model.criterion.get_assigned_targets_and_loss(s,batch)[0][0]
            norm=positives.sum().clamp_min(1)
        target=t['scores'].float().detach().sigmoid()
        qfl=(F.binary_cross_entropy_with_logits(scores,target,reduction='none')*(scores.sigmoid()-target).abs()).sum()/norm
        kd=F.kl_div(boxes.reshape(bs,4,head.reg_max,-1).log_softmax(2),
                    t['boxes'].float().detach().reshape(bs,4,head.reg_max,-1).softmax(2),reduction='none').sum(2).mean(1)
        weights=target.max(1).values
        reg=(kd*weights).sum()/weights.sum().clamp_min(1e-6)
        self.last_audit={'qfl':float(qfl.detach()),'dfl_kl':float(reg.detach()),'positive_count':int(norm),'teacher_conf_mass':float(weights.sum())}
        return qfl+4*reg

    def d0_detection_loss(self,s,t,batch):
        """Same-location D0 detector targets; I1 supplies J0's mask target."""
        sc=self.student_model.criterion
        with torch.no_grad():
            detached={k:v.detach() if isinstance(v,torch.Tensor) else v for k,v in s.items()}
            fg,gi,gb,anchor,stride=sc.get_assigned_targets_and_loss(detached,batch)[0]
        zero=s['scores'].float().sum()*0
        bi,ai=fg.nonzero(as_tuple=True)
        if not len(ai):
            self._j0_detection_audit={'positive_anchors':0,'GT_with_positive':0}
            return zero,zero
        bs=len(batch['img']);device=batch['img'].device
        assert t['scores'].shape==s['scores'].shape and t['boxes'].shape==s['boxes'].shape
        assert torch.equal(self.teacher_model.model[-1].stride,self.student_model.model[-1].stride)
        assert self.teacher_model.model[-1].reg_max==self.student_model.model[-1].reg_max
        img_hw=torch.tensor(s['feats'][0].shape[2:],device=device,dtype=s['scores'].dtype)*sc.stride[0]
        targets=torch.cat((batch['batch_idx'].view(-1,1),batch['cls'].view(-1,1),batch['bboxes']),1)
        packed=sc.preprocess(targets.to(device),bs,img_hw[[1,0,1,0]])
        cls=packed[...,0].long()[bi,gi[bi,ai].long()]
        assert torch.all((cls>=0)&(cls<s['scores'].shape[1]))
        slogit=s['scores'].permute(0,2,1)[bi,ai,cls].float()
        tprob=t['scores'].permute(0,2,1)[bi,ai,cls].float().detach().sigmoid()
        pair=bi*(packed.shape[1]+1)+gi[bi,ai].long()
        unique,inverse,counts=torch.unique(pair,return_inverse=True,return_counts=True)
        weight=counts[inverse].float().reciprocal()/len(unique)
        cls_loss=(F.binary_cross_entropy_with_logits(slogit,tprob,reduction='none')*weight).sum()
        sb=sc.bbox_decode(anchor,s['boxes'].permute(0,2,1).float())[bi,ai]*stride[ai]
        with torch.no_grad():
            tb=sc.bbox_decode(anchor,t['boxes'].permute(0,2,1).float().detach())[bi,ai]*stride[ai]
        scale=torch.tensor([img_hw[1],img_hw[0],img_hw[1],img_hw[0]],device=device)
        box_loss=(F.smooth_l1_loss(sb/scale,tb/scale,reduction='none',beta=.02).mean(-1)*weight).sum()
        self._j0_detection_audit={'positive_anchors':len(ai),'GT_with_positive':len(unique),
                                  'cls_term':float(cls_loss.detach()),'box_term':float(box_loss.detach())}
        return cls_loss,box_loss

    def instance_loss(self,s,t,batch):
        sc=self.student_model.criterion
        if self._teacher_criterion is None: self._teacher_criterion=self.teacher_model.init_criterion()
        with torch.no_grad():
            fg,gi,gb,anchor,stride=sc.get_assigned_targets_and_loss(s,batch)[0]
            tf,tgi,*_=self._teacher_criterion.get_assigned_targets_and_loss(t,batch)[0]
            tb=sc.bbox_decode(anchor,t['boxes'].permute(0,2,1).float())*stride
        sb=sc.bbox_decode(anchor,s['boxes'].permute(0,2,1).float())*stride
        zero=s['scores'].float().sum()*0
        terms=[zero,zero,zero]; mass=[0.,0.,0.]; eligible=0; matched=0
        h,w=batch['img'].shape[-2:]; mh,mw=batch['masks'].shape[-2:]
        scale=sb.new_tensor([w,h,w,h]); yy=torch.arange(mh,device=sb.device)[:,None]; xx=torch.arange(mw,device=sb.device)[None,:]
        for b in range(len(batch['img'])):
            for g in gi[b,fg[b]].unique():
                g=int(g); eligible+=1
                pos=torch.where(fg[b] & (gi[b]==g))[0]
                gt=gb[b,pos[0]]; cls=int(batch['cls'][batch['batch_idx']==b][g])
                candidates=torch.where(tf[b] & (tgi[b]==g))[0]
                if not len(candidates): continue
                with torch.no_grad():
                    quality=elementwise_iou(tb[b,candidates],gt)
                    a=int(candidates[quality.argmax()]); tq=elementwise_iou(tb[b,a],gt)
                    if tq<=.5 or int(t['scores'][b,:,a].argmax())!=cls: continue
                    sq=elementwise_iou(sb[b,pos].detach(),gt)
                    wdet=tq*torch.sigmoid((tq-sq)/.05)
                    prob=t['scores'][b,cls,a].float().sigmoid()
                matched+=1
                terms[0]=terms[0]+(F.binary_cross_entropy_with_logits(s['scores'][b,cls,pos].float(),prob.expand(len(pos)),reduction='none')*wdet).mean()
                terms[1]=terms[1]+(F.smooth_l1_loss(sb[b,pos]/scale,(tb[b,a]/scale).expand(len(pos),4),beta=.02,reduction='none').mean(1)*wdet).mean()
                mass[0]+=float(wdet.mean()); mass[1]+=float(wdet.mean())
                rep=int(pos[(((anchor*stride)[pos]-(gt[:2]+gt[2:])/2).square().sum(1)).argmin()])
                truth=batch['masks'][b]==g+1
                roi=(xx>=gt[0]*mw/w)&(xx<gt[2]*mw/w)&(yy>=gt[1]*mh/h)&(yy<gt[3]*mh/h)
                if not bool(truth.any() and roi.any()): continue
                sl=torch.einsum('c,chw->hw',s['mask_coefficient'][b,:,rep].float(),s['proto'][b].float())
                with torch.no_grad():
                    tl=torch.einsum('c,chw->hw',t['mask_coefficient'][b,:,a].float(),t['proto'][b].float())
                    truth=truth&roi; sm=(sl.detach().sigmoid()>.5)&roi; tm=(tl.sigmoid()>.5)&roi
                    sq=(sm&truth).sum()/(sm|truth).sum().clamp_min(1)
                    tq=(tm&truth).sum()/(tm|truth).sum().clamp_min(1)
                    wm=tq*torch.sigmoid((tq-sq)/.05) if tq>.5 else tq*0
                terms[2]=terms[2]+F.binary_cross_entropy_with_logits(sl[roi],tl.sigmoid()[roi])*wm
                mass[2]+=float(wm)
        terms=[x/max(eligible,1) for x in terms]
        self.last_audit={'eligible_GT':eligible,'teacher_qualified_GT':matched,
            'effective_mass':[x/max(eligible,1) for x in mass],
            'terms':[float(x.detach()) for x in terms]}
        # I1 is a one-factor removal of I0's teacher true-class BCE.
        # Keep computing the term for audit; exclude it from the gradient.
        if self.mode=='J0':
            return terms[2]
        if self.mode=='I1':
            return 5*terms[1]+terms[2]
        return terms[0]+5*terms[1]+terms[2]

    def loss(self,batch,preds=None):
        self._student_feats.clear(); self._teacher_feats.clear()
        if self.training and self.kd_enabled:
            with torch.no_grad(): t=self.teacher_model(batch['img'])[1]
        s=self.student_model(batch['img']) if preds is None else preds
        native,items=self.student_model.loss(batch,s)
        kd=native.sum()*0
        if self.training and self.kd_enabled:
            with torch.autocast(device_type=batch['img'].device.type,enabled=False):
                if self.mode=='J0':
                    cls,box=self.d0_detection_loss(s,t,batch)
                    mask=self.instance_loss(s,t,batch)
                    self.last_audit['d0_detection']=self._j0_detection_audit
                    kd=(cls+5*box+mask)*self.kd_scale
                else:
                    kd=(self.cross_loss(s,t,batch) if self.mode=='X0' else self.instance_loss(s,t,batch))*self.kd_scale
        assert torch.isfinite(kd), 'nonfinite transfer loss'
        items['transfer_loss']=kd.detach()
        return torch.cat((native,(kd*len(batch['img'])).reshape(1))),items
