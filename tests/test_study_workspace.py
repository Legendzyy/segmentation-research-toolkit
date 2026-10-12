"""Study state safety and handoff checks; no ML dependencies."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from tools.study import add_stage, checkpoint, initialize, status


class StudyWorkspace(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.intake = ('邻近实例分离', '研究者指定的公开数据集', '一张 GPU；显存与时限待核实')
        initialize(self.root, 'study_a', *self.intake)
        self.path = self.root / 'studies/study_a'

    def snapshot(self):
        return (self.path / 'STUDY_STATE.json').read_bytes()

    def update(self):
        return {'status': 'exploring', 'summary': '仅检查工作区；未执行实验。',
                'next_action': '核对数据集协议。', 'evidence': [], 'blockers': [], 'running_jobs': []}

    def test_intake_is_preserved_without_inventing_protocol(self):
        state = status(self.root, 'study_a')
        self.assertEqual(tuple(state['intake'].values()), self.intake)
        protocol = json.loads((self.path / 'engineering/eng00_baseline/configs/protocol.json').read_text(encoding='utf-8'))
        self.assertEqual(protocol['status'], 'draft')
        self.assertIsNone(protocol['dataset']['manifest'])
        self.assertIsNone(protocol['baseline']['implementation'])
        self.assertIsNone(protocol['budget']['seeds'])
        self.assertEqual((self.path / 'engineering/eng00_baseline/run_registry.jsonl').read_text(), '')
        self.assertFalse((self.root / 'work').exists())

    def test_duplicate_and_escape_leave_original_untouched(self):
        before = self.snapshot()
        for name in ['study_a', '../outside', 'CON', 'nul', 'bad/name']:
            with self.assertRaises(ValueError):
                initialize(self.root, name, *self.intake)
        self.assertEqual(before, self.snapshot())
        with self.assertRaises(ValueError):
            add_stage(self.root, 'study_a', 'engineering', '../escape', 'question')
        self.assertEqual(before, self.snapshot())

    def test_new_stage_and_switch_do_not_rewrite_previous_results(self):
        old = self.path / 'engineering/eng00_baseline/results/observations.json'
        old.write_text('{"observed": false}')
        add_stage(self.root, 'study_a', 'diagnostics', 'p01_errors', '哪些错误可重复？')
        self.assertTrue((self.path / 'diagnostics/p01_errors/DIAGNOSTIC_CONTRACT.md').is_file())
        self.assertEqual(status(self.root, 'study_a')['active_stage']['path'], 'diagnostics/p01_errors')
        update = self.update()
        update['stage'] = 'engineering/eng00_baseline'
        checkpoint(self.root, 'study_a', update)
        self.assertEqual(old.read_text(), '{"observed": false}')
        state = json.loads(self.snapshot())
        self.assertEqual(len(state['stages']), 2)
        self.assertEqual([event['type'] for event in state['events']], ['init', 'stage', 'checkpoint'])

    def test_evidence_is_hashed_and_changes_are_visible_after_resume(self):
        proof = self.path / 'engineering/eng00_baseline/results/inspection.json'
        proof.write_text('{"type":"workspace_check"}')
        update = self.update()
        update['evidence'] = [proof.relative_to(self.root).as_posix()]
        checkpoint(self.root, 'study_a', update)
        self.assertEqual(status(self.root, 'study_a')['evidence_missing_or_changed'], [])
        resume = (self.path / 'engineering/eng00_baseline/RESUME.md').read_text(encoding='utf-8')
        self.assertIn(update['next_action'], resume)
        proof.write_text('{}')
        self.assertEqual(status(self.root, 'study_a')['evidence_missing_or_changed'], update['evidence'])
        proof.unlink()
        self.assertEqual(status(self.root, 'study_a')['evidence_missing_or_changed'], update['evidence'])

    def test_invalid_checkpoint_cannot_advance_state(self):
        before = self.snapshot()
        variants = [
            {'status': 'complete'}, {'status': 'running'}, {'status': 'blocked'},
            {'evidence': ['missing.json']}, {'evidence': ['../outside.json']},
            {'running_jobs': [{'id': '123'}]}, {'unexpected': True},
        ]
        for patch in variants:
            update = copy.deepcopy(self.update()); update.update(patch)
            with self.assertRaises(ValueError):
                checkpoint(self.root, 'study_a', update)
            self.assertEqual(self.snapshot(), before)

    def test_live_job_handoff_and_study_isolation(self):
        initialize(self.root, 'study_b', *self.intake)
        second = (self.root / 'studies/study_b/STUDY_STATE.json').read_bytes()
        update = self.update()
        update.update(status='running', running_jobs=[{'host': 'test-host', 'id': 'scheduler-123', 'command': 'example-only', 'output': 'work/study_a/run01'}])
        result = checkpoint(self.root, 'study_a', update)
        self.assertEqual(result['active_stage']['running_jobs'], update['running_jobs'])
        add_stage(self.root, 'study_a', 'diagnostics', 'p01_errors', '待检验问题')
        self.assertEqual(status(self.root, 'study_a')['registered_jobs'][0]['id'], 'scheduler-123')
        self.assertEqual((self.root / 'studies/study_b/STUDY_STATE.json').read_bytes(), second)


if __name__ == '__main__':
    unittest.main()
