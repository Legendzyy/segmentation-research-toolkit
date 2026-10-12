"""Create an unfilled research stage without running or freezing an experiment."""

import argparse
import json
import re
from pathlib import Path


RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))}


def create_stage(root, kind, name):
    root = Path(root).resolve(strict=True)
    if kind not in {"diagnostics", "engineering"}:
        raise ValueError("Kind must be diagnostics or engineering")
    if not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", name) or name in RESERVED:
        raise ValueError("Use a non-reserved lowercase stage name of 2-64 characters")
    parent = root / kind
    if parent.is_symlink() or parent.resolve() != parent or not parent.is_dir():
        raise ValueError("Stage parent must be an ordinary directory in this repository")
    destination = parent / name
    if destination.exists():
        raise ValueError("Refusing to overwrite an existing stage")
    mapping = {"PROTOCOL.md": "PROTOCOL.md", "EXPERIMENT_LOG.md": "EXPERIMENT_LOG.md",
               "DECISION.md": "DECISIONS.md", "CLAIM_EVIDENCE.md": "CLAIM_EVIDENCE.md"}
    # Read all sources before creating anything; a missing template leaves no stage.
    files = {target: (root / "templates" / source).read_text(encoding="utf-8").replace("<stage_id>", name)
             for source, target in mapping.items()}
    config = json.loads((root / "configs/experiment.example.json").read_text(encoding="utf-8"))
    config.update(experiment_id=name, status="DRAFT", execution_authorized=False)
    config["data"]["final_content_access_authorized"] = False
    files["config.json"] = json.dumps(config, indent=2, ensure_ascii=False) + "\n"
    files["README.md"] = (f"# {name}\n\n状态：DRAFT，尚未定义或执行研究。\n\n"
                          "先填写 [协议](PROTOCOL.md) 与 [配置](config.json)，再接入自己的实现。\n\n"
                          "记录 [日志](EXPERIMENT_LOG.md)、[决策](DECISIONS.md) 与 "
                          "[claim 映射](CLAIM_EVIDENCE.md)。工具没有自动冻结或数据访问功能。\n")
    destination.mkdir()
    for filename, content in files.items():
        (destination / filename).write_text(content, encoding="utf-8", newline="\n")
    for folder, content in {"src": "阶段实现入口；不在 import 时启动实验。",
                            "results": "小型聚合结果；发布前审核，不存原始数据与样本身份。"}.items():
        (destination / folder).mkdir()
        (destination / folder / "README.md").write_text(content + "\n", encoding="utf-8", newline="\n")
    return {"stage": destination.relative_to(root).as_posix(), "status": "DRAFT",
            "execution_started": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("diagnostics", "engineering"))
    parser.add_argument("name")
    args = parser.parse_args()
    try:
        result = create_stage(Path(__file__).resolve().parents[1], args.kind, args.name)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Stage error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
