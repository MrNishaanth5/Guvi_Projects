import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms
import torchvision.models as models
import numpy as np
from PIL import Image

st.title("🕊️Aerial Object Classification🚁")
st.header("📝Instruction")
st.write("• Upload only JPG, JPEG or PNG images")
st.write("• Click **Predict** For Identifiction")

images=st.file_uploader("Upload",type=["jpg", "jpeg", "png"],accept_multiple_files=True)
if images:
    for img in images:
        Image.open(img).convert("RGB")

transform=transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
    ])

model=models.resnet50(weights=None)
model.fc=nn.Linear(model.fc.in_features,1)

model.load_state_dict(torch.load("r_best_model.pth",map_location="cpu"))
model.eval()

button=st.button("Predict")

if button:
    if images:
        for image in images:
            st.image(image)
            img=Image.open(image).convert("RGB")
            img=transform(img).unsqueeze(0)
            with torch.no_grad():
                logits=model(img)
                pred= torch.sigmoid(logits)
            label="Drone" if pred >=0.5 else "Bird"
            confidence= pred*100 if pred >=0.5 else (1-pred)*100
            conf=np.round(float(confidence),2)
            st.write(f"Label: {label}")
            st.write(f"Confidence Score:{conf}")
    else:
        st.write("⚠️ Upload your Images")
# Feedback
st.markdown("#### Rating:")
feedback=st.feedback("stars")
if feedback is not None:
    st.markdown("##### 💐Thank You for Rating✨")