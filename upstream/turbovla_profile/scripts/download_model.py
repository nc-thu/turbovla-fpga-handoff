import os,sys,traceback
os.environ["REQUESTS_CA_BUNDLE"]="/etc/ssl/certs/ca-certificates.crt"
os.environ["HF_HUB_DISABLE_TELEMETRY"]="1"
from huggingface_hub import snapshot_download
try:
 print("START",flush=True)
 p=snapshot_download("H-EmbodVis/TurboVLA",local_dir="pretrained/TurboVLA",allow_patterns=["checkpoints/libero/turbovla_libero.pth","libero_all4_stats.json","config.json","config.yaml","DINOv3_LICENSE.md","LICENSE","README.md"],max_workers=2)
 print("DONE",p,flush=True)
except Exception:
 traceback.print_exc();sys.exit(1)