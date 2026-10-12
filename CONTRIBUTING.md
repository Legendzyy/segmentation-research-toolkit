# 维护说明

本仓库的主体是作者原生研究资产。修改阅读说明时请链接支持它的具体原件；不要把推断写成原报告事实，也不要补造数据或已经执行的实验。

阶段原件保持历史内容。若确需更正原报告，保留原版本、添加具日期的更正说明，并更新来源映射；不要改结果来配合论文叙事。新增研究使用新阶段，重新确定科学定义和执行授权。

提交前运行 `python tools/verify_archive.py` 和 `python -m unittest discover -s tests -v`；训练/评价修改另跑真实数据 smoke。移植代码变更需更新 `evidence/CODE_SOURCE_MAP.json` 的 hash 与适配说明。新增公开内容逐文件核对来源和范围；`.gitignore` 不是发布审查的替代。数据、权重、逐样本缓存及明确排除的在研资料不进入仓库。代码许可见 `THIRD_PARTY_NOTICES.md`。
