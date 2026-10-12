"""Run actual train/save/load/evaluate/replay for each port on prepared public smoke data."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from research_toolkit.io import fresh_directory, write_json
from research_toolkit.models import VARIANTS


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--variants',nargs='+',default=VARIANTS)
    args=parser.parse_args()
    folder=fresh_directory(args.output)
    data=str(Path(args.data).resolve())
    config=Path(__file__).resolve().parents[1]/'configs/runnable/smoke.json'
    teacher=folder/'teacher'
    def execute(label,command):
        with (folder/(label+'.log')).open('w',encoding='utf-8') as stream:
            subprocess.run([sys.executable,'-m','research_toolkit',*command],stdout=stream,stderr=subprocess.STDOUT,check=True)
    execute('teacher',['train','--config',str(config),'--scale','s','--data',data,'--output',str(teacher)])
    records=[]
    for variant in args.variants:
        label=variant.replace(':','_');run=folder/label;evaluation=folder/(label+'_eval')
        record=dict(variant=variant,status='RUNNING');records.append(record)
        write_json(folder/'validation.json',records)
        try:
            command=['train','--config',str(config),'--variant',variant,'--data',data,'--output',str(run)]
            if variant.startswith(('eng02:','eng03:','eng04:')):
                command+=['--teacher',str(teacher/'deploy.pt')]
            execute(label,command)
            execute(label+'_deploy',['check-deploy','--run',str(run)])
            execute(label+'_eval',['evaluate','--run',str(run),'--data',data,'--output',str(evaluation),'--reference-size','64'])
            execute(label+'_replay',['replay','--evaluation',str(evaluation)])
            record.update(status='PASS',train_epochs=1,input_size=64,reference_size=64,checkpoint_sha256=json.loads((run/'completion.json').read_text())['checkpoint_sha256'])
        except Exception:
            record['status']='FAILED';write_json(folder/'validation.json',records);raise
        write_json(folder/'validation.json',records)
        print(f'PASS {variant}: train/save/load/evaluate/replay',flush=True)


if __name__=='__main__':main()
