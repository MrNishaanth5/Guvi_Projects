from ultralytics import YOLO
import matplotlib.pyplot as plt

model=YOLO("best.pt")

results= model.predict(source="D:\Guvi\Fruit Object Detection\samples",
                       save=False)

i=1
plt.figure(figsize=(12,8))

for img in results:
    image=img.plot()

    plt.subplot(2,2,i)
    plt.imshow(image)
    plt.axis("off")
    i=i+1
plt.tight_layout()
plt.show()