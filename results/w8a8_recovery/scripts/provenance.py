"""Read-only provenance capture; never reads credentials or environment secrets."""
import datetime,hashlib,importlib.metadata,json,subprocess
from pathlib import Path
from run_recovery import SOURCE,PRETRAIN,CKPT
import argparse

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()

def main(root):
    paths=[CKPT,SOURCE/'experiments/libero/configs/libero_all4_stats.json']
    for directory in ('dinov3_local','bert_local'):
        paths+=[p for p in (PRETRAIN/'assets'/directory).rglob('*') if p.is_file()]
    paths+=list((root/'scripts').glob('*.py'))+list((root/'observations').glob('*.pt'))
    if (root/'calibration.pt').exists():paths.append(root/'calibration.pt')
    result={'generated':datetime.datetime.now().isoformat(timespec='seconds'),
      'source_commit':subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip(),
      'source_changes':subprocess.check_output(['git','-C',str(SOURCE),'status','--short'],text=True),
      'files':{str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths},
      'packages':{p.metadata['Name']:p.version for p in importlib.metadata.distributions() if p.metadata['Name']},
      'gpu':subprocess.check_output(['nvidia-smi','--query-gpu=index,name,memory.free,utilization.gpu','--format=csv'],text=True)}
    try:
        result['libero_commit']=subprocess.check_output(['git','-C','/home/nc23/workspace/LIBERO','rev-parse','HEAD'],text=True).strip()
        result['libero_changes']=subprocess.check_output(['git','-C','/home/nc23/workspace/LIBERO','status','--short'],text=True)
    except subprocess.CalledProcessError as exc:result['libero_git_error']=str(exc)
    (root/'provenance.json').write_text(json.dumps(result,indent=2))
    print('hashed',len(paths),'files')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);main(p.parse_args().root)
