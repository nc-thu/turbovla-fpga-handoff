import argparse,datetime,json,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);args=p.parse_args()
start=datetime.datetime.now().isoformat(timespec='seconds');t=time.perf_counter()
data=json.loads(subprocess.check_output([sys.executable,str(args.root/'scripts/test_quant_core.py')],text=True))
data.update(started=start,finished=datetime.datetime.now().isoformat(timespec='seconds'),elapsed_s=time.perf_counter()-t)
(args.root/'integer_unit_checks_final.json').write_text(json.dumps(data,indent=2))
print(json.dumps(data,indent=2))
