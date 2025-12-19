---
title: Fruit Object Detection
emoji: 🍎
colorFrom: green
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 🍎🍌🍊 Fruit Object Detection using YOLOv8

This project implements **fruit detection (Apple, Banana, Orange)** using **Ultralytics YOLOv8**.  
The dataset contains images of three classes and was trained, validated, and tested using custom augmentation.  
The final model is deployed with a **Streamlit App** and hosted on **AWS/GCP** for real-time inference.

---

## 📌 **Project Overview**

This project identifies three fruit classes:

- **Apple (class 0)**
- **Banana (class 1)**
- **Orange (class 2)**  

## 📁 Project Structure

project/
├── yolo_data/
│   ├── images/
│   │   ├── train/
│   │   ├── valid/
│   │   ├── test/
│   ├── labels/
│   │   ├── train/
│   │   ├── valid/
│   │   ├── test/
├── best.pt
├── fruit_streamlit.py
└── data.yaml


---

## 🚀 Model Summary

- Model: **YOLOv8s**
- Epochs: **80**
- Device: **Google Colab GPU**
- Early stopping enabled
- Augmentation applied:
  - Horizontal Flip  
  - Brightness/Contrast  
  - Rotation  
  - Color Jitter  
  - Motion/Motion Blur  
  - Random Shadows  
- **Number of classes = 3**  
  - apple  
  - banana  
  - orange  

---

## 📊 Final Evaluation Metrics

Your final training metrics (real values):

### **Per-Class Scores**
| Class   | Precision | Recall | F1-Score |
|---------|-----------|--------|----------|
| Apple   | **0.95194** | **0.96000** | **0.95595** |
| Banana  | **0.98054** | **0.78261** | **0.87047** |
| Orange  | **0.98089** | **0.93333** | **0.95652** |

---

### **Mean Scores**
| Metric     | Value |
|------------|--------|
| **mAP50**      | **0.96237** |
| **mAP50-95**   | **0.71713** |

---

## 🔲 Confusion Matrix

Your final confusion matrix:
[[24  0  0  1]
 [ 0  21 1  7]
 [ 1  0  14 0]
 [ 0  2  0  0]]

---
