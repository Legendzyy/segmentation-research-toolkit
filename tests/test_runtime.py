import copy
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import torch
from research_toolkit.evaluate import encode, coco_metrics, rasterize
from research_toolkit.boundary import balanced_boundary_loss, instance_boundary_target
from research_toolkit.feature_kd import ENG02FeatureDistiller
from research_toolkit.ablation import summarize
from research_toolkit.data import polygons, prepare
from research_toolkit.io import write_json


class RuntimeContracts(unittest.TestCase):
    def test_empty_predictions_and_exact_segmentation(self):
        mask=np.zeros((64,64),np.uint8);mask[10:30,20:40]=1
        gt=dict(info={},images=[dict(id=1,width=64,height=64)],categories=[dict(id=1,name='object')],annotations=[dict(id=1,image_id=1,category_id=1,segmentation=encode(mask),area=400,bbox=[20,10,20,20],iscrowd=0)])
        self.assertEqual(coco_metrics(gt,[])['AP'],0.)
        prediction=[dict(image_id=1,category_id=1,score=.9,segmentation=encode(mask))]
        self.assertAlmostEqual(coco_metrics(gt,prediction)['AP'],1.)
        gt['images'].append(dict(id=2,width=64,height=64))
        missing=copy.deepcopy(gt['annotations'][0]);missing.update(id=2,image_id=2);gt['annotations'].append(missing)
        self.assertLess(coco_metrics(gt,prediction)['AP'],.51)

    def test_reference_raster_matches_native_formula(self):
        import cv2
        xy=np.array([[.125,.1],[.75,.1],[.75,.8]],dtype=np.float64)
        expected=np.zeros((640,640),np.uint8)
        cv2.fillPoly(expected,[(xy*[320,160]*2+[0,160]).astype(np.int32)],1)
        np.testing.assert_array_equal(rasterize(xy,320,160,640),expected)

    def test_boundary_padding_has_no_gradient(self):
        logits=torch.zeros(1,1,4,4,requires_grad=True)
        target=torch.zeros(1,4,4);target[:,1,1]=1
        valid=torch.ones_like(target);valid[:,:,3]=0
        loss=balanced_boundary_loss(logits,target,valid);loss.backward()
        self.assertTrue(torch.all(logits.grad[:,:,:,3]==0))
        self.assertGreater(float(logits.grad.abs().sum()),0.)
        target,valid=instance_boundary_target([], (64,64),np.zeros((64,64),np.uint8))
        self.assertEqual(float(target.sum()+valid.sum()),0.)

    def test_feature_weight_mass_and_empty_boxes(self):
        batch=dict(img=torch.zeros(2,3,64,64),bboxes=torch.tensor([[.5,.5,.25,.25]]),batch_idx=torch.tensor([0]))
        weights=ENG02FeatureDistiller._foreground_weights(batch,8,8,torch.float32)
        torch.testing.assert_close(weights.mean((2,3)),torch.ones(2,1))
        self.assertGreater(float(weights[0,0,3,3]),float(weights[0,0,0,0]))
        torch.testing.assert_close(weights[1],torch.ones(1,8,8))

    def test_invalid_polygon_is_not_silently_clipped(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'label.txt';p.write_text('0 -0.01 0 1 0 1 1')
            with self.assertRaises(ValueError):polygons(p,1)

    def test_duplicate_train_val_is_rejected(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            for split in ['train','val']:
                (d/split).mkdir();Image.new('RGB',(32,32)).save(d/split/'a.png')
                (d/split/'a.txt').write_text('0 .1 .1 .8 .1 .8 .8')
            with self.assertRaisesRegex(ValueError,'Duplicate image'):
                prepare(d/'train',d/'train',d/'val',d/'val',['object'],d/'prepared')

    def test_pairing_rejects_mixed_protocol(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            base=dict(variant='native',seed=42,dataset_manifest_sha256='x',protocol={'reference_size':640},role='engineering_smoke',run_config={'scale':'n','epochs':1,'batch':2,'imgsz':64,'weights':'none','initialization_sha256':None},metrics={k:0. for k in ['AP','AP50','AP75','AP90','AP_small','AP_medium','AP_large']})
            candidate=copy.deepcopy(base);candidate.update(variant='eng01:E4');candidate['protocol']['reference_size']=64
            write_json(d/'base.json',base);write_json(d/'candidate.json',candidate)
            with self.assertRaisesRegex(ValueError,'Incompatible protocol'):
                summarize([d/'base.json',d/'candidate.json'],'native',d/'summary')
            candidate['protocol']=copy.deepcopy(base['protocol'])
            base['run_config']['teacher_sha256']='teacher-A'
            candidate['run_config']['teacher_sha256']='teacher-B'
            write_json(d/'base.json',base);write_json(d/'candidate.json',candidate)
            with self.assertRaisesRegex(ValueError,'Different teacher'):
                summarize([d/'base.json',d/'candidate.json'],'native',d/'summary')

    def test_kd_matrix_preflight_before_baseline_training(self):
        from research_toolkit.matrix import run
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            write_json(d/'matrix.json',dict(variants=['native','eng03:D0'],seeds=[42],baseline='native',training={}))
            with self.assertRaisesRegex(ValueError,'requires an existing'):
                run(d/'matrix.json',d/'missing-data.yaml',d/'run')
            self.assertFalse((d/'run').exists())


if __name__=='__main__':unittest.main()
