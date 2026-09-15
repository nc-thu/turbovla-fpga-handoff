import os
os.environ["REQUESTS_CA_BUNDLE"]="/etc/ssl/certs/ca-certificates.crt"
from huggingface_hub import snapshot_download
for rid in ["facebook/dinov3-vitb16-pretrain-lvd1689m","google-bert/bert-base-uncased"]:
 try:
  p=snapshot_download(rid,local_dir="pretrained/assets/"+rid.replace('/','_'),allow_patterns=["config.json","preprocessor_config.json","tokenizer.json","tokenizer_config.json","vocab.txt","model.safetensors","pytorch_model.bin","special_tokens_map.json"],max_workers=2)
  print(rid,p,flush=True)
 except Exception as e: print(type(e).__name__,rid,e,flush=True)