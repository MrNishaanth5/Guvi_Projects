import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

st.title("🍎Fruit Object Detection🍏")
st.header("📝Instruction")
st.write("• Upload only JPG, JPEG or PNG images")
st.write("• Click **Detect** For Identifiction")

model=YOLO("best.pt")

images=st.file_uploader("Upload your Image",accept_multiple_files=True,type=["jpg","jpeg","png"])

button= st.button("Detect")

if button:
    for image in images:
        image=Image.open(image)
        image=np.array(image)
        pred=model(image)
        img=pred[0].plot()
        st.image(img)

        