> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# ENG02 efficiency evidence

All four new formal training jobs ran on the shared RTX 4060 alongside an independent ICASSP project at varying utilization. Process time and PyTorch peak **allocated** VRAM are observations, not controlled throughput or total-device-memory comparisons. A0 is the audited read-only ENG01 E0 checkpoint and adds no ENG02 training job.

| Model | Deployed network; input | Native model parameters | Native model summary FLOPs | Formal training process time | Peak allocated training VRAM |
|---|---|---:|---:|---:|---:|
| A0 reused E0 | YOLO11n-seg; 640 | 2,842,998 | 9.8 GFLOPs (native model summary) | historical 8512 s | historical 2.074 GiB |
| A1 | YOLO11n-seg; 896 | 2,842,998 | 9.8 GFLOPs model-summary figure; **not** a verified 896-input FLOP count | 9328 s | 4.062 GiB |
| A2 | YOLO11s-seg; 640 | 10,083,062 | 33.2 GFLOPs (native model summary) | 9019 s | 3.104 GiB |
| K1 | YOLO11n-seg; 640; teacher/adapters training-only | 2,842,998 | 9.8 GFLOPs | 8851 s | 2.168 GiB |
| K2 | YOLO11n-seg; 640; teacher/adapters training-only | 2,842,998 | 9.8 GFLOPs | 8837 s | 2.169 GiB |

Fused model summaries report 2,834,958 parameters/9.6 GFLOPs for native n and 10,067,590/32.9 GFLOPs for native s. Those are not measurements of end-to-end preprocessing, postprocessing, mask reconstruction or latency. K1/K2 final checkpoint payloads are native student segmentation models; the s teacher and three 1×1 adapters are absent from deployment. Accordingly neither KD variant has a demonstrated deployed parameter/FLOP reduction relative to A0. No controlled isolated batch-1 latency was obtained, so efficiency route P3 cannot be claimed. An isolated timing campaign was conditional on a qualifying final candidate and is not warranted at K2/STOP.

Formal ENG02 training total: A1 9328 + A2 9019 + K1 8851 + K2 8837 = **36,035 process seconds, 10.01 process hours**, four new full training tasks of the 19-task/72-hour ceilings. Values derive from `runs/*/completion.json`; historic A0 is excluded. No test data were used.
