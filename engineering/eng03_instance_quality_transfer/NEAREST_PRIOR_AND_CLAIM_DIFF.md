> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Targeted prior and claim difference — development position

This is a design comparison, **not** a novelty certificate. ENG01's broader
technical-neighbor inventory and ENG02's KD review are inherited read-only;
only the nearest mechanisms to ENG03's proposed output KD are listed here.

| Work | Established idea | Consequence for ENG03 |
|---|---|---|
| [FGD, CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Yang_Focal_and_Global_Knowledge_Distillation_for_Detectors_CVPR_2022_paper.html) | Foreground/background focal feature imitation with spatial/channel attention and a global relation term. | ENG02 K2's normalized 2:1 foreground MSE was **not** full FGD. ENG03 cannot claim first spatially selective KD. If FGD is a comparator, implement its relevant terms faithfully or label a simplification. |
| [GID, CVPR 2021](https://openaccess.thecvf.com/content/CVPR2021/html/Dai_General_Instance_Distillation_for_Object_Detection_CVPR_2021_paper.html) | Select discriminative teacher instances and combine instance-level feature, relation and response transfer, including beyond a simple GT-positive split. | ENG03 cannot claim first instance selection or first response KD. Its possible difference is a GT-corresponded native instance-mask output path and separately judged tasks; this still requires direct evidence. |
| [ICD, NeurIPS 2021](https://proceedings.neurips.cc/paper/2021/hash/892c91e0a653ba19df81a90f89d99bcd-Abstract.html) | Instance-conditional extraction of knowledge useful to classification and localization. | Task-aware/instance-aware KD is prior art. ENG03 must explain the actual correspondence and mask-specific target/gradient path, not rename conditional KD. |
| [CrossKD, CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_CrossKD_Cross-Head_Knowledge_Distillation_for_Object_Detection_CVPR_2024_paper.html) | Send student intermediate head features through the frozen teacher head; prediction imitation can avoid contradictory native-head supervision. | The closest mature detection-output contrast. ENG03 direct output KD is *not* CrossKD. If adapting CrossKD, the frozen teacher-head parameters must still backpropagate to student features. A segmentation-mask extension would be an adaptation, not proof of a new general principle. |
| [MasKD, ICLR 2023](https://arxiv.org/abs/2205.14589) | Learn receptive-token spatial masks to select feature distillation regions. | Its “mask” is a feature-region selection mask, not necessarily a decoded per-instance segmentation mask. ENG03 must not conflate the two. |
| [LD, CVPR 2022](https://openaccess.thecvf.com/content/CVPR2022/html/Zheng_Localization_Distillation_for_Dense_Object_Detection_CVPR_2022_paper.html) | Distill localization distributions in separately chosen spatial regions; classification/localization targets need different treatment. | Separate localization KD and region selection are established. YOLO11 teacher/student have the same stride/reg_max only if checked at runtime; otherwise use a decoded-box target. |
| [BCKD, ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/html/Yang_Bridging_Cross-task_Protocol_Inconsistency_for_Distillation_in_Dense_Object_Detection_ICCV_2023_paper.html) | Address the mismatch between dense detection's independent sigmoid class protocol and class-softmax KD. | ENG03 uses independent sigmoid/BCE targets for the true class and must never use a one-class softmax KL. |
| [Hierarchical Distillation, ICCV Workshops 2019](https://openaccess.thecvf.com/content_ICCVW_2019/html/TASK-CV/Deng_Towards_Efficient_Instance_Segmentation_with_Hierarchical_Distillation_ICCVW_2019_paper.html) | Instance-segmentation-specific hierarchical teacher–student transfer includes mask-head/channel information. | ENG03 cannot claim the first segmentation-specific or mask-aware KD; its testable difference is rendered GT-corresponded masks jointly organized with detector outputs in a native YOLO head. A direct architectural match is still untested. |
| [Guided Distillation, WACV 2024](https://openaccess.thecvf.com/content/WACV2024/html/Berrada_Guided_Distillation_for_Semi-Supervised_Instance_Segmentation_WACV_2024_paper.html) | Teacher guidance with a burn-in strategy for limited-label semi-supervised instance segmentation. | It establishes teacher-guided instance segmentation as prior art, but has a different label-access problem and training protocol; no reported AP from it is comparable to ENG03's fully supervised Blueberry split. |
| [Training a Student Expert via Semi-Supervised Foundation Model Distillation, CVPRW 2026](https://openaccess.thecvf.com/content/CVPR2026W/ECV/html/Taghavi_Training_a_Student_Expert_via_Semi-Supervised_Foundation_Model_Distillation_CVPRW_2026_paper.html) | Transfers VFM knowledge to a smaller instance-segmentation student using supervised/pseudo-label objectives and an instance-aware pixel contrastive term. | Its instance-aware class/mask transfer limits broad novelty wording. Its semi-supervised VFM/contrastive mechanism differs from ENG03's same-augmentation dense GT-anchor response KD, but a concrete empirical distinction has not yet been established. |

The proposed experiment changes the **supervision object** from K1/K2's
uniform neck-feature residual to common-grid class/box logits and rendered
instance-mask outputs tied to training GT. A second optional change selects
teacher transfer separately by task using detached train-GT quality. Native
GT loss remains. No candidate-index pairing across post-NMS model queues,
prototype-channel regression, val-derived training weights, or additional
inference module is proposed.

The nearest direct benchmark is plain class+box+mask output KD under the same
training budget, then a faithful CrossKD-style detection-head adaptation if
the implementation and budget permit. The selective rule was measured in
Q0/M0/C0 and **did not establish a repeatable advantage** over plain D0.
Without a positive contrast to simple output KD and a faithful nearest
mature adaptation, the fair claim is an implemented local engineering
adaptation with an unresolved efficacy question. Detection papers' COCO box
AP cannot be copied as instance-mask AP.

The September 2026 targeted refresh above checks direct task overlap, not all
recent segmentation KD work. It does not certify absence of another closer
method. The closest direct **mechanism** comparisons remain simple
multi-output KD and a faithful task-prediction-path adaptation such as
CrossKD; the instance-segmentation papers above constrain claim scope.

## 2026-09-27 outcome and targeted primary-source recheck

The D0/Q0/M0/C0/R0/F0 contrasts and two matched native seeds are now measured in ENG03. Task-specific selection, ranked mask-anchor choice and simple addition to ordinary feature MSE did **not** establish a repeatable advantage. Therefore no ENG03 novelty or utility claim is promoted, and no faithful mature adaptation is called defeated. CrossKD's official paper routes student head features through a frozen teacher head for prediction imitation; this differs from our native-head GT-linked response target and would need a separate faithful segmentation adaptation. GID's official paper already combines discriminative instance selection with feature, relation and response KD; our instance-selection terminology cannot be a novelty claim. The 2019 instance-segmentation H-Dis paper already studies hierarchical representation and head-level transfer, including mask knowledge. Primary sources rechecked: [CrossKD](https://arxiv.org/abs/2306.11369), [GID](https://arxiv.org/abs/2103.02340), and [Hierarchical Distillation](https://openaccess.thecvf.com/content_ICCVW_2019/papers/TASK-CV/Deng_Towards_Efficient_Instance_Segmentation_with_Hierarchical_Distillation_ICCVW_2019_paper.pdf). This is targeted overlap checking, not exhaustive prior-art clearance.
