"""Finish numeric audits after the sequential GPU benchmark releases its device."""
import argparse,datetime,json,subprocess,sys,time
from pathlib import Path

def main(root):
    t=time.monotonic()
    while not (root/'pipeline_complete.json').exists():
        if time.monotonic()-t>4*3600:raise RuntimeError('Software pipeline did not finish; inspect its logs')
        time.sleep(10)
    selected=json.loads((root/'frozen_candidate.json').read_text())['candidate']
    stages=[('fixed_replay','run_recovery.py',['--stage','replay','--modes',selected+'_fixed']),
            ('integer_audit','integer_audit.py',[]),('hardware_cost','hardware_cost.py',[]),
            ('provenance','provenance.py',[]),('report','report.py',[])]
    for name,script,options in stages:
        start=datetime.datetime.now().isoformat(timespec='seconds');tic=time.monotonic()
        with (root/'logs'/('post_'+name+'.log')).open('w') as f:
            rc=subprocess.call([sys.executable,'-u',str(root/'scripts'/script),'--root',str(root),*options],stdout=f,stderr=subprocess.STDOUT)
        event={'stage':'post_'+name,'start':start,'end':datetime.datetime.now().isoformat(timespec='seconds'),
               'elapsed_s':time.monotonic()-tic,'returncode':rc}
        with (root/'stage_events.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
        print(event,flush=True)
        if rc:raise RuntimeError('Postflight stage failed: '+name)
    (root/'postflight_complete.json').write_text(json.dumps({'finished':datetime.datetime.now().isoformat(timespec='seconds')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);main(p.parse_args().root)
