# 安装与首次运行

开展自己的课题时，先按[新课题工作区](NEW_STUDY.md)提供场景、数据集和算力，由 Agent 创建独立阶段。以下安装与工程检查可在协议尚未确定时先完成；新课题输出使用自己的 `work/<study>/` 路径。

## 环境

Python 3.10–3.12，Git。测试运行使用 Python 3.12、PyTorch 2.5.1 / torchvision 0.20.1 CPU。模型内部 API 固定到 Ultralytics commit `b454f423600f99d41730bd75a7a26b491187de36`，不要替换为任意最新版。

```bash
git clone https://github.com/Legendzyy/segmentation-research-toolkit.git
cd segmentation-research-toolkit
python -m venv .venv
```

Linux/macOS 激活：`source .venv/bin/activate`。Windows PowerShell 激活：`.\.venv\Scripts\Activate.ps1`；若本机限制激活脚本，可直接使用 `.\.venv\Scripts\python.exe` 代替下文 `python`。

CPU 安装：

```bash
python -m pip install --upgrade pip
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python -m pip install -e .
python -m research_toolkit variants
```

CUDA 环境先从 [PyTorch 既往版本安装页](https://pytorch.org/get-started/previous-versions/)选择与驱动匹配的 2.5.1 / 0.20.1 构建，再安装本仓库 requirements。正式配置中的 `device: "0"` 表示单张 CUDA 卡；CPU 使用 `"cpu"`。多卡训练未接入。

## 运行真实公开小数据

```bash
python -m research_toolkit fetch-smoke --output work/coco8
python -m research_toolkit matrix --config configs/runnable/smoke_matrix.json --data work/coco8/prepared/data.yaml --output work/smoke_matrix
python -m research_toolkit replay --evaluation work/smoke_matrix/native_s42_eval
python -m research_toolkit check-deploy --run work/smoke_matrix/eng01_E4_s42
```

第一条下载官方 COCO8-seg，生成经核对的 train/val 副本与 manifest。第二条在独立进程中顺序训练 native 和 ENG01 E4，每项 CPU、64 输入、1 epoch、batch 2，然后计算同协议 COCO mask AP 并汇总。第三条从保存的 GT/预测重算 AP；第四条核对移除辅助头前后的 CPU 输出逐值一致，预期均为 `status: PASS`。

预期文件：

```text
work/smoke_matrix/
  matrix.json                 # 原始矩阵
  queue.json                  # 逐任务 PASS / FAILED
  native_s42.log              # 原始 stdout/stderr
  native_s42/run.json         # 解析后的配置与身份 hash
  native_s42/deploy.pt        # 去除教师/辅助头的部署模型
  native_s42/completion.json  # 最后预定 epoch 的完成记录
  native_s42_eval/metrics.json
  native_s42_eval/gt.json
  native_s42_eval/predictions.json
  summary/paired.csv          # 同 seed 候选−baseline 百分点差
```

小数据上的 AP 可能为 0；这些值用于检查管线，不用于判断模块优劣。工程测试与历史科研结果严格分开。

## 接入自己的公开数据副本

从[数据说明](DATASETS.md)取得数据，保持明确的训练与验证身份。YOLO 分割标签每行为 `class x1 y1 x2 y2 ...`，类别从 0 开始，坐标归一化。类别名按 ID 顺序提供：

```bash
python -m research_toolkit prepare-yolo --train-images /path/images/train --train-labels /path/labels/train --val-images /path/images/val --val-labels /path/labels/val --names class0 class1 --output work/mydata
python -m research_toolkit train --config configs/runnable/eng01.json --variant eng01:E1 --data work/mydata/data.yaml --output work/e1_s42
python -m research_toolkit evaluate --run work/e1_s42 --data work/mydata/data.yaml --output work/e1_s42_eval
```

将 `/path/...` 和类别名替换为实际值。准备器会复制文件，避免训练框架的标签缓存写回原数据；拒绝 train/val 内容重复、缺失标签、非法类别和越界坐标。背景图必须具有空标签文件。准备器不自动生成随机划分、不扫描 test。

## 训练教师与执行 KD

```bash
python -m research_toolkit train --config configs/runnable/eng01.json --variant native --scale s --weights yolo11s-seg.pt --data work/mydata/data.yaml --output work/teacher_s42
python -m research_toolkit train --config configs/runnable/eng03.json --variant eng03:D0 --teacher work/teacher_s42/deploy.pt --data work/mydata/data.yaml --output work/d0_s42
python -m research_toolkit evaluate --run work/d0_s42 --data work/mydata/data.yaml --output work/d0_s42_eval
```

教师应在同任务训练，类别数量与映射必须一致。预训练权重可由上游下载；本仓库不附带任何历史权重。教师训练成本应计入实验报告。

完整的家族消融配置见 `configs/runnable/eng02_matrix.json`、`eng03_matrix.json`、`eng04_matrix.json`、`p1f_matrix.json`。例如：

```bash
python -m research_toolkit matrix --config configs/runnable/eng04_matrix.json --teacher work/teacher_s42/deploy.pt --data work/mydata/data.yaml --output work/eng04_matrix
```

矩阵是新实验的显式对照安排，不复用历史阶段的自适应停止或确认身份。若要以另一变体为参照，可以对已有 `metrics.json` 使用 `summarize --baseline VARIANT --metrics FILE... --output NEW_DIR`，无需重新训练。

## 故障处理

| 报错 | 操作 |
|---|---|
| 缺少 `DistillationModel` / prediction dict API | 重装 requirements 中固定 commit，不安装任意 Ultralytics 版本 |
| Output already exists | 检查已有完成/失败记录，使用新目录；不覆盖、不自动恢复 |
| Missing label / invalid coordinate / duplicate image | 修正数据准备定义并重新导出副本，不静默跳过样本 |
| Teacher class count/names differ | 使用与学生相同类别映射训练的教师 |
| CUDA OOM / batch changed | 新运行中显式修改 batch，并给比较组同样配置 |
| Manifest/hash changed | 数据或 checkpoint 已变；重新准备一个可识别的新实验 |

检查命令：`python -m unittest discover -s tests -v`、`python tools/verify_archive.py`。科学结果以正式数据、完整预算和预先定义的比较为依据。
