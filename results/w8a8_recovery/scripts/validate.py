"""Dataset separation and accounting checks; no success-rate cherry-picking."""
import argparse,datetime,json,math
from pathlib import Path

def main(root,complete=False):
    rows=[json.loads(p.read_text()) for p in (root/'episodes').glob('*.json')]
    keyed={(r['mode'],r['suite'],r['task'],r['initial_state_id']):r for r in rows}
    checks={'unique_episode_keys':len(keyed)==len(rows),
            'native_chunk_12':all(r.get('chunk_size')==12 for r in rows),
            'no_program_errors':all(r['status'] in ('success','task_failure') for r in rows)}
    for name in ('fp32','observe'):
        path=root/'replay'/(name+'.json')
        checks[name+'_unchanged']=path.exists() and json.loads(path.read_text())['max']==0
    for path in (root/'replay').glob('*.json'):
        r=json.loads(path.read_text())
        checks['finite_'+r['mode']]=math.isfinite(r['mae']) and math.isfinite(r['max']) and all(
            math.isfinite(s['mae']) and math.isfinite(s['max']) for s in r['samples'])
        if r['mode'] in ('observe','fp32','attention_only','activation_only','weight_only') or r['n']!=144:continue
        checks['coverage_'+r['mode']]=r['calls']=={'linear':44208,'conv2d':288,
            'attention_qk':6048,'attention_av':6048,'bmm':3456,'baddbmm':864}
        checks['width_'+r['mode']]=all(x['a_bits']==8 and x['b_bits']==8 for x in r['operators'].values())
    frozen=root/'frozen_candidate.json';pairs=0
    if frozen.exists():
        f=json.loads(frozen.read_text());selected=f['candidate']
        held=[r for r in rows if r['initial_state_id']>=3]
        checks['frozen_before_holdout']=all(r['started']>=f['frozen_at'] for r in held)
        checks['only_frozen_model_on_holdout']=all(r['mode'] in ('fp32',selected) for r in held)
        checks['holdout_not_calibration']=all(3<=r['initial_state_id']<=22 for r in held)
        mismatch=[]
        for r in held:
            if r['mode']!=selected:continue
            b=keyed.get(('fp32',r['suite'],r['task'],r['initial_state_id']))
            if b:
                pairs+=1
                if any(r[k]!=b[k] for k in ('seed','initial_state_sha256','chunk_size')):mismatch.append(r)
        checks['paired_scenes_and_seeds']=not mismatch
        dev_hashes={r['initial_state_sha256'] for r in rows if r['initial_state_id']<3}
        checks['no_identical_initial_state_in_development']=not dev_hashes.intersection(r['initial_state_sha256'] for r in held)
    if complete:
        checks['all_160_pairs']=pairs==160
        checks['all_464_episodes']=len(rows)==464
        checks['software_pipeline_finished']=(root/'pipeline_complete.json').exists()
        prov=root/'provenance.json'
        if prov.exists():
            weights=[v['sha256'] for k,v in json.loads(prov.read_text())['files'].items() if k.endswith('/turbovla_libero.pth')]
            checks['checkpoint_unchanged']=weights==['d031ad7be05a2f5d04afb3194ed26b0cb46083685edee7a5e145078a37d26bab']
        else:checks['checkpoint_unchanged']=False
    result={'generated':datetime.datetime.now().isoformat(timespec='seconds'),
            'complete_requested':complete,'episodes':len(rows),'pairs':pairs,'checks':checks,'pass':all(checks.values())}
    (root/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['pass']:raise RuntimeError('Validation failed; do not claim complete')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--complete',action='store_true')
    args=p.parse_args();main(args.root,args.complete)
