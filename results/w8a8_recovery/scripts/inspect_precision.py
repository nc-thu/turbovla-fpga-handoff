import argparse,json,torch
from pathlib import Path
from run_recovery import CKPT
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);args=p.parse_args()
c=torch.load(CKPT,map_location='cpu',weights_only=False)
cfg=c.get('model_config',{})
result={'checkpoint_model_config':cfg,'reference_override':'vision.compute_precision = fp32; parameters=float32; TF32 disabled',
        'interaction_checkpoint_precision':cfg.get('interaction',{}).get('compute_precision','fp32')}
(args.root/'precision_audit.json').write_text(json.dumps(result,indent=2,default=str))
print(json.dumps(result,indent=2,default=str))
assert result['interaction_checkpoint_precision']=='fp32'
