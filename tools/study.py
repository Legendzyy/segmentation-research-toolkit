"""Create and resume native-style research stages. Standard library only; MIT."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
STATUSES = ('planning', 'exploring', 'running', 'analyzing', 'blocked', 'complete')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def slug(value):
    if not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', value):
        raise ValueError('Use a lowercase identifier: letter followed by letters, digits, _ or - (max 64).')
    if value.split('.')[0] in {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)), *(f'lpt{i}' for i in range(1, 10))}:
        raise ValueError('Reserved Windows identifier.')
    return value


def nonempty(value):
    if not value.strip():
        raise ValueError('Text must not be empty.')
    return value.strip()


def inside(root, path):
    root = root.resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(root) or resolved == root:
        raise ValueError('Path must stay inside its workspace.')
    return resolved


def study_path(root, name):
    return inside(root, root / 'studies' / slug(name))


def write_json(path, value):
    """Replace one state file atomically, including on Windows."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def scaffold(path, files):
    """Build in a sibling temporary directory; never overwrite an existing stage."""
    if path.exists():
        raise ValueError(f'Already exists: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.study-build-', dir=path.parent) as temporary:
        source = Path(temporary) / 'content'
        source.mkdir()
        for name, content in files.items():
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        source.rename(path)


def stage_files(kind, question):
    contract = 'ENGINEERING_CONTRACT.md' if kind == 'engineering' else 'DIAGNOSTIC_CONTRACT.md'
    return {
        'README.md': f'# 阶段入口\n\n研究问题：{question}\n\n先读 `RESUME.md`，再读 `{contract}`、`configs/protocol.json` 和 `EXECUTION_JOURNAL.md`。状态以课题根目录 `STUDY_STATE.json` 为准。\n',
        contract: '# 阶段协议\n\n状态：draft；尚未执行正式实验。\n\n本阶段问题：' + question + '\n\n'
            '协议定义见 `configs/protocol.json`。先核对官方数据角色、评价实现、baseline 配方与资源，再填写数据身份、主指标、预算和对照。未知项保持 null，不能从历史阶段推定。\n\n'
            '探索与正式比较分开记录。能够由当前任务或既有协议唯一确定的选择直接落实；会改变科学结论且仍有歧义的选择集中向研究者确认，同时继续环境检查等独立工作。\n\n'
            '冻结时保存协议 hash、代码 commit 和配置到实际运行记录；修改科学定义时保留旧版本并记录理由。是否执行由当前任务授权决定，draft 文档本身不授权正式训练或访问封存数据。\n',
        'METHOD_SPEC.md': '# 方法定义\n\n状态：未提出新方法。\n\n先复现强 baseline 并记录具体错误，再定义待检验的机制。每个候选明确输入/输出、连接位置、计算、训练/推理差异、参数与计算成本、对照和可推翻解释的证据。事实、假设和已确认机制分开书写。\n',
        'configs/protocol.json': json.dumps({
            'schema': 1, 'status': 'draft', 'question': question,
            'dataset': {'source': None, 'version': None, 'license': None, 'manifest': None, 'split_roles': None, 'class_mapping': None},
            'baseline': {'implementation': None, 'revision': None, 'initialization': None, 'recipe': None},
            'evaluation': {'implementation': None, 'primary_endpoint': None, 'secondary_endpoints': [], 'test_access': 'not_authorized_by_scaffold'},
            'budget': {'device': None, 'epochs': None, 'batch': None, 'imgsz': None, 'seeds': None, 'max_gpu_hours': None},
            'comparison_matrix': [], 'checkpoint_policy': None,
            'freeze_record': None,
        }, ensure_ascii=False, indent=2) + '\n',
        'configs/README.md': '# 配置\n\n`protocol.json` 是研究协议草案，不能直接传给训练 CLI。正式运行另存 `train.json` / `matrix.json`，沿用仓库 `configs/runnable/` 的运行 schema；明确检查适配范围后填写当前课题选择。不要把旧阶段预算自动当作本课题预算。\n',
        'analysis/README.md': '# 分析\n\n保存错误类型、混杂因素、替代解释和下一项区分实验；每项观察引用真实运行与样本来源。诊断未完成时不写成机制结论。\n',
        'results/README.md': '# 结果\n\n仅放经过核对的紧凑汇总与证据索引，注明数据、协议、seed、代码版本和来源。数据、checkpoint、逐样本预测和长日志放仓库 `work/<study>/<stage>/<run>/`，不自动发布。未执行项明确写未执行。\n',
        'src/README.md': '# 阶段代码\n\n稳定运行能力优先复用 `src/research_toolkit/`。本目录仅保存本阶段的适配、诊断或候选实现；改变模型或评价定义时补充针对性验证，并保留与 baseline 的可比性。\n',
        'paper/PAPER_BLUEPRINT.md': '# 论文主线\n\n状态：无新实验结论。\n\n按场景困难、强 baseline 的实际局限、针对性机制、公平比较、模块/交互贡献、成本与适用范围组织。每个 claim 关联结果文件；失败和未排除解释保留在阶段报告中。\n',
        'FINAL_REPORT.md': '# 阶段报告\n\n状态：尚未结束，无结果。\n\n结束时填写实际完成内容、支持与不支持的主张、异常、失败、计算成本及下一阶段建议，并链接协议和证据。行政性关闭不等于方法有效。\n',
        'EXECUTION_JOURNAL.md': '# 执行日志\n\n尚无执行。按时间追加实际命令、工作目录、环境、进程/任务标识、输出路径、失败及处置；不要把计划写成执行。结构化接续事件保存在课题 `STUDY_STATE.json` 的 events 中。\n',
        'run_registry.jsonl': '',
        'artifact_index.json': '{"schema": 1, "artifacts": []}\n',
    }


def stage_record(path, question):
    return {'path': path, 'question': question, 'status': 'planning',
            'summary': '阶段已创建；尚无实验或结论。',
            'next_action': '核对环境、数据官方协议与资源；跑通工程 smoke，再建立当前课题的 baseline 协议。',
            'evidence': [], 'blockers': [], 'running_jobs': [], 'updated_at': now()}


def render_resume(path, state):
    # A derived view. STUDY_STATE.json remains authoritative if writing this fails.
    for stage in state['stages']:
        target = inside(path, path / stage['path'])
        content = f"# 阶段接续\n\n由工具生成；直接编辑会在下次 checkpoint 时被覆盖。权威状态：课题根目录 `STUDY_STATE.json`。\n\n更新时间：{stage['updated_at']}\n\n状态：{stage['status']}\n\n已知事实：{stage['summary']}\n\n下一步：{stage['next_action']}\n\n"
        content += '```json\n' + json.dumps({k: stage[k] for k in ('evidence', 'blockers', 'running_jobs')}, ensure_ascii=False, indent=2) + '\n```\n\n'
        content += '继续前先检查在跑任务是否仍存在、输出是否变化和已有 failure/completion 记录；不要重复启动。旧进程记录不是仍在运行的证据。\n'
        (target / 'RESUME.md').write_text(content, encoding='utf-8')


def initialize(root, name, scenario, dataset, compute):
    path = study_path(root, name)
    intake = {key: nonempty(value) for key, value in [('scenario', scenario), ('dataset', dataset), ('compute', compute)]}
    stage = 'engineering/eng00_baseline'
    question = '在指定场景和 benchmark 上建立强 baseline，识别可重复的错误与质量/成本取舍。'
    state = {'schema': 1, 'study_id': name, 'intake': intake, 'active_stage': stage,
             'stages': [stage_record(stage, question)], 'events': []}
    state['events'].append({'time': now(), 'type': 'init', 'stage': stage, 'intake': intake})
    files = {
        'STUDY_STATE.json': json.dumps(state, ensure_ascii=False, indent=2) + '\n',
        'README.md': f'# {name}\n\n当前状态见 `STUDY_STATE.json`，当前阶段见其中 `active_stage`。在仓库根目录运行 `python tools/study.py status --study {name}`。\n\n原始需求见 `USER_REQUEST.md`；阶段按 `engineering/` 和 `diagnostics/` 组织。运行输出位于仓库 `work/{name}/`。\n',
        'USER_REQUEST.md': '# 新课题输入\n\n以下是研究者提供的场景、数据集与算力描述；数据名称不构成下载许可，资源描述需在运行环境核实。\n\n```json\n' + json.dumps(intake, ensure_ascii=False, indent=2) + '\n```\n',
        'DECISIONS.md': '# 决策记录\n\n目前仅建立独立研究阶段；尚未选择或冻结 baseline、数据划分、主指标和预算。后续按日期追加问题、证据、决策、替代解释与科学定义是否变化。\n',
        'AGENTS.md': '# Study execution contract\n\n'
            'Follow the repository root AGENTS.md, then read STUDY_STATE.json, USER_REQUEST.md, DECISIONS.md and the active stage RESUME.md, contract and configs/protocol.json. Paths in state are relative to this study; run CLI commands from the repository root.\n\n'
            'The three intake fields are user context, not a frozen protocol. Inspect environment and official dataset/baseline documentation; verify benchmark roles and available compute. Run the repository engineering smoke independently of unresolved scientific choices. Derive a concrete baseline plan from evidence. Ask only about unresolved scientific ambiguity or missing required authorization; continue independent work. Do not presume an old module is suitable before diagnosing the new baseline.\n\n'
            'Track runs in the active stage run_registry.jsonl with command, cwd, seed, code commit, config/manifest/checkpoint hashes, output path and actual status. Track live jobs by host and process/scheduler ID; check existing output and process status before launching anything. Do not convert a running or failed run into a completed result.\n\n'
            'At handoff, record commands and failures in EXECUTION_JOURNAL.md, decisions in DECISIONS.md, and use tools/study.py checkpoint to update authoritative state and derived RESUME.md. Register compact evidence with paths and hashes; bulk artifacts stay under work/. Root PROJECT_STATE.json describes toolkit capabilities, not this study. Never overwrite historical archives. Publication requires the current user scope; creating a study does not authorize publishing its research.\n',
    }
    files.update({f'{stage}/{key}': value for key, value in stage_files('engineering', question).items()})
    scaffold(path, files)
    render_resume(path, state)
    return status(root, name)


def load(root, name):
    path = study_path(root, name)
    state = json.loads((path / 'STUDY_STATE.json').read_text(encoding='utf-8'))
    if state.get('schema') != 1 or state.get('study_id') != name:
        raise ValueError('Invalid study state identity/schema.')
    paths = [s['path'] for s in state['stages']]
    if len(paths) != len(set(paths)) or state['active_stage'] not in paths:
        raise ValueError('Invalid active stage or duplicate stage.')
    for stage in state['stages']:
        if not inside(path, path / stage['path']).is_dir() or stage['status'] not in STATUSES:
            raise ValueError('Invalid stage directory/status.')
    return path, state


def status(root, name):
    path, state = load(root, name)
    stage = next(s for s in state['stages'] if s['path'] == state['active_stage'])
    changed = []
    for item in stage['evidence']:
        file = inside(root, root / item['path'])
        if not file.is_file() or file_hash(file) != item['sha256']:
            changed.append(item['path'])
    return {'study': path.relative_to(root).as_posix(), 'intake': state['intake'], 'active_stage': stage,
            'registered_jobs': [{'stage': s['path'], **job} for s in state['stages'] for job in s['running_jobs']],
            'evidence_missing_or_changed': changed, 'state': 'STUDY_STATE.json',
            'read_next': [f"{stage['path']}/{name}" for name in ['RESUME.md', 'configs/protocol.json', 'EXECUTION_JOURNAL.md']]}


def add_stage(root, name, kind, identifier, question):
    path, state = load(root, name)
    relative = f'{kind}/{slug(identifier)}'
    if kind not in ('engineering', 'diagnostics'):
        raise ValueError('Invalid stage kind.')
    question = nonempty(question)
    scaffold(inside(path, path / relative), stage_files(kind, question))
    state['stages'].append(stage_record(relative, question))
    state['active_stage'] = relative
    state['events'].append({'time': now(), 'type': 'stage', 'stage': relative, 'question': question})
    write_json(path / 'STUDY_STATE.json', state)
    render_resume(path, state)
    return status(root, name)


def checkpoint(root, name, value):
    path, state = load(root, name)
    allowed = {'stage', 'status', 'summary', 'next_action', 'evidence', 'blockers', 'running_jobs'}
    if set(value) - allowed or not allowed - {'stage'} <= value.keys():
        raise ValueError('Checkpoint requires status, summary, next_action, evidence, blockers, running_jobs; optional stage.')
    relative = value.get('stage', state['active_stage'])
    stage = next((s for s in state['stages'] if s['path'] == relative), None)
    if stage is None or value['status'] not in STATUSES:
        raise ValueError('Unknown stage or invalid status.')
    for key in ('summary', 'next_action'):
        nonempty(value[key])
    if not all(isinstance(value[k], list) for k in ('evidence', 'blockers', 'running_jobs')):
        raise ValueError('evidence, blockers and running_jobs must be arrays.')
    if not all(isinstance(item, str) and item.strip() for item in value['blockers']):
        raise ValueError('blockers must contain nonempty strings.')
    if value['status'] == 'blocked' and not value['blockers']:
        raise ValueError('Blocked status needs a concrete blocker.')
    for job in value['running_jobs']:
        if not isinstance(job, dict) or not all(isinstance(job.get(k), str) and job[k].strip() for k in ('host', 'id', 'command', 'output')):
            raise ValueError('Each live job needs host, id, command and output strings.')
    if value['status'] == 'running' and not value['running_jobs']:
        raise ValueError('Running status needs a process/scheduler record.')
    if value['status'] == 'complete' and (value['running_jobs'] or value['blockers'] or not value['evidence']):
        raise ValueError('Complete needs evidence and no live jobs/blockers; this does not validate a scientific claim.')
    evidence = []
    for entry in value['evidence']:
        if not isinstance(entry, str):
            raise ValueError('Evidence must be repository-relative file paths.')
        file = inside(root, root / entry)
        if not file.is_file():
            raise ValueError(f'Missing evidence: {entry}')
        evidence.append({'path': file.relative_to(root).as_posix(), 'sha256': file_hash(file)})
    update = {**value, 'evidence': evidence, 'updated_at': now()}
    update.pop('stage', None)
    stage.update(update)
    state['active_stage'] = relative
    state['events'].append({'time': now(), 'type': 'checkpoint', 'stage': relative, **update})
    write_json(path / 'STUDY_STATE.json', state)
    render_resume(path, state)
    return status(root, name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('init')
    for field in ('study', 'scenario', 'dataset', 'compute'):
        p.add_argument('--' + field, required=True)
    p = sub.add_parser('status'); p.add_argument('--study', required=True)
    p = sub.add_parser('stage'); p.add_argument('--study', required=True)
    p.add_argument('--kind', choices=['engineering', 'diagnostics'], required=True)
    p.add_argument('--id', required=True); p.add_argument('--question', required=True)
    p = sub.add_parser('checkpoint'); p.add_argument('--study', required=True); p.add_argument('--input', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'init':
            result = initialize(ROOT, args.study, args.scenario, args.dataset, args.compute)
        elif args.command == 'stage':
            result = add_stage(ROOT, args.study, args.kind, args.id, args.question)
        elif args.command == 'checkpoint':
            result = checkpoint(ROOT, args.study, json.loads(Path(args.input).read_text(encoding='utf-8-sig')))
        else:
            result = status(ROOT, args.study)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f'ERROR: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
