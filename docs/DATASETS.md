# 数据集获取与接入

核对日期：2026-10-12。数据由使用者从官方渠道取得，仓库不镜像图像、标签或测试集。数据许可独立于代码许可。

## Mega_Blueberry

[MegaFruits 官方项目](https://github.com/wyn-Mandy/MegaFruits)提供数据说明、引用和使用条件；其下载入口指向 [Kaggle MegaFruits](https://www.kaggle.com/datasets/mmwang0/megafruits)。在平台登录并按其要求取得 **Mega_Blueberry** 子集。不要将整个数据集合并进本项目，也不需要下载其他水果子集。

官方说明标注为 YOLO 格式。取得文件后检查具体版本的目录、类别映射与 train/val/test 定义，使用 `prepare-yolo` 显式指定图像和 polygon 标签目录；命令见 [首次运行](START_HERE.md)。如果所选导出只有 bbox 四元组，该导出不能用于当前分割训练，应取得分割 polygon 版本。

官方条款限制非商业用途并禁止再分发原数据或其修改副本；本仓库仅提供来源和接入代码。使用时按官方要求引用并致谢。Kaggle 下载可能需要登录或接受条款，本仓库不保存账号、API key 或提供绕过方式。

历史报告中的 1778 train / 254 val 是原研究使用的数据视图。本仓库未发布其样本身份清单；仅有相同数量不能证明复现了该划分。新数据必须重新生成 manifest，使用自己的实验 ID 和结果。

## MinneApple

[作者仓库](https://github.com/nicolaihaeni/MinneApple)链接到 [University of Minnesota 数据记录](https://hdl.handle.net/11299/206575)。从数据记录取得 detection/segmentation 图像与掩码，保留原数据角色；下载文件和适用条款以该记录为准。本次浏览器无法展开数据门户内容，未验证压缩包下载，不提供猜测的文件直链。

其[原生 loader](https://github.com/nicolaihaeni/MinneApple/blob/master/data/apple_dataset.py)读取 `images/` 和 `masks/`，以非零像素 ID 区分实例。该格式不是当前 runner 的 YOLO polygon 输入。直接采用官方 Mask R-CNN 入口，或在独立数据准备步骤转换并验证 mask 等价后再接入；多连通区域、孔洞或极小实例不能静默变成单个外轮廓。本仓库尚未验证该转换，因此不把 MinneApple 标为已跑通的数据适配器。

历史阶段只登记过条件性 MinneApple 验证计划，没有实际完成相应结果；原报告中未运行的行仍保持未运行。

## COCO8-seg：工程 smoke

小规模真实数据来自固定 Ultralytics 源码的 [coco8-seg.yaml](https://github.com/ultralytics/ultralytics/blob/b454f423600f99d41730bd75a7a26b491187de36/ultralytics/cfg/datasets/coco8-seg.yaml)所列[公开资产](https://github.com/ultralytics/assets/releases/download/v0.0.0/coco8-seg.zip)。运行 `fetch-smoke` 自动下载到显式目录，记录 ZIP SHA256，并生成 train/val manifest。

COCO8-seg 只用于安装、训练、保存、评价和消融管线验证。它不是强 benchmark，不足以支撑方法比较；其数据许可与引用遵循上游说明。
