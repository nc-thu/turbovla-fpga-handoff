"""Sequential GPU experiment stages. Exit on error; never retune on holdout."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

def run(root,label,*options):
    log=root/'logs'/(label+'.log')
    start=datetime.datetime.now().isoformat(timespec='seconds');t=time.perf_counter()
    with log.open('w') as f:
        rc=subprocess.call([sys.executable,'-u',str(Path(__file__).with_name('run_recovery.py')),
                            '--root',str(root),*options],stdout=f,stderr=subprocess.STDOUT)
    event={'stage':label,'start':start,'end':datetime.datetime.now().isoformat(timespec='seconds'),
           'elapsed_s':time.perf_counter()-t,'returncode':rc}
    with (root/'stage_events.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
    print(event,flush=True)
    if rc:raise RuntimeError('Stage failed; inspect '+str(log))

def rates(root,name):
    rows=[json.loads(p.read_text()) for p in (root/'episodes').glob(name+'_*.json')]
    rows=[r for r in rows if r['mode']==name and r['initial_state_id']<3]
    if len(rows)!=24 or any(r['status'] not in ('success','task_failure') for r in rows):
        raise RuntimeError('Incomplete candidate '+name)
    suites=sorted({r['suite'] for r in rows})
    return sum(r['success'] for r in rows),{s:sum(r['success'] for r in rows if r['suite']==s) for s in suites}

def main(root):
    # Baseline capture is started separately; confirm completion before running.
    rows=list((root/'episodes').glob('fp32_*.json'))
    if len(rows)!=24:raise RuntimeError('Strict FP32 capture must finish first')
    for name in ('legacy_fp32','legacy_w8a8'):
        run(root,name,'--mode',name)
    for name in ('fp32','observe','tensor','token','smooth_0.25','smooth_0.5','smooth_0.75','group_128','group_64','group_32'):
        run(root,'replay_'+name,'--stage','replay','--modes',name)
        if name in ('fp32','observe'):
            check=json.loads((root/'replay'/(name+'.json')).read_text())
            # Exact no-op should be bitwise. Observer decomposes conv, hence
            # must be checked quantitatively before accepting calibration.
            threshold=0. if name=='fp32' else 1e-5
            if check['max']>threshold:raise RuntimeError('Observer/pass-through changed output: '+str(check['max']))
    group_names=sorted(('group_128','group_64','group_32'),key=lambda n:json.loads((root/'replay'/(n+'.json')).read_text())['mae'])[:2]
    for n in group_names:run(root,'replay_'+n+'_mse','--stage','replay','--modes',n+'_mse')
    for n in ('weight_only','activation_only','attention_only'):
        run(root,'diagnostic_'+n,'--stage','replay','--modes',n)
    eligible=['tensor','token','smooth_0.25','smooth_0.5','smooth_0.75','group_128','group_64','group_32']+[n+'_mse' for n in group_names]
    records={n:json.loads((root/'replay'/(n+'.json')).read_text()) for n in eligible}
    scale_cost=lambda n:sum(r['scale_values_per_call'] for r in records[n]['operators'].values())
    finalists=sorted(eligible,key=lambda n:(records[n]['mae'],records[n]['max'],scale_cost(n),n))[:3]
    (root/'development_selection.json').write_text(json.dumps({'candidates':finalists,'rule':'MAE,max,scale_count,name'},indent=2))
    for n in finalists:run(root,'screen_'+n,'--mode',n)
    base,bs=rates(root,'fp32')
    def score(n):
        total,ss=rates(root,n)
        return (-total,max(bs[s]-ss[s] for s in bs),scale_cost(n),n)
    selected=min(finalists,key=score)
    frozen={'candidate':selected,'fp32_development_success':base,'selected_development_success':rates(root,selected)[0],
            'frozen_at':datetime.datetime.now().isoformat(timespec='seconds'),'holdout_initial_states':list(range(3,23))}
    (root/'frozen_candidate.json').write_text(json.dumps(frozen,indent=2))
    for name in ('fp32',selected):
        for suite in ('libero_spatial','libero_object','libero_goal','libero_10'):
            # Keep every unit bounded to ten episodes; no truncated episode.
            for start in (3,8,13,18):
                run(root,f'holdout_{name}_{suite}_{start}','--mode',name,'--suites',suite,'--start',str(start),'--end',str(start+5))
    (root/'pipeline_complete.json').write_text(json.dumps({'finished':datetime.datetime.now().isoformat(timespec='seconds'),'selected':selected},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    main(p.parse_args().root)
