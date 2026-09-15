import torch,json,os
p="pretrained/TurboVLA/checkpoints/libero/turbovla_libero.pth"
c=torch.load(p,map_location="cpu",weights_only=True); st=c["model_state_dict"]
for n,t in st.items():
 if n.startswith("vision_encoder") or n.startswith("text_encoder"):
  print(n,tuple(t.shape),t.dtype)