"""Read-only preparation for Claude: inventory exact inputs and clock/host evidence."""
import argparse,datetime,hashlib,json,re,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
root=args.repo.resolve();args.out.mkdir(parents=True,exist_ok=True)
paths=[root/'compiler/v7_2026-09-10_1258_f4_ybase_pong/sw/compiler.py',root/'hw/v8_2026-09-12_0054_rtl_util_r5/rtl_p2/ae_gemm_p2d.sv',root/'hw/v10_2026-09-12_1148_engfull_preadd/notes/regression_verdict.md']
records=[]
for p in paths:
 b=p.read_bytes();t=b.decode('utf-8-sig',errors='replace')
 records.append({'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(),'matching_lines':[{'line':i,'text':line} for i,line in enumerate(t.splitlines(),1) if re.search(r'HostOp|host_gemm|deform_host|input\s+logic\s+c?clk|create_generated_clock|FAIL|ALL PASS',line)]})
try:
 inventory=subprocess.run(['rg','--files','--hidden','--no-ignore','compiler','hw/v10_2026-09-12_1148_engfull_preadd'],cwd=root,text=True,capture_output=True,check=True).stdout.splitlines()
except (OSError,subprocess.CalledProcessError):inventory=[]
selected=[p for p in inventory if Path(p).name in ['host_plan.json','model_summary.json','ops_trace.json','manifest.json'] or p.endswith(('.rpt','.xdc','.tcl'))]
report={'generated':datetime.datetime.now().isoformat(),'read_only':True,'records':records,'candidate_inputs':selected,'warning':'Static references are not dynamic operator coverage. Select the actual compiled build and join its host plan to the model trace.'}
(args.out/'input_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(f'Wrote {args.out / "input_audit.json"}; {len(selected)} candidate input/report files; no experiment launched.')
