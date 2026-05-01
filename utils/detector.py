```python
from ultralytics import YOLO

model = YOLO("models/yolov8n-face.pt")

def detect_face(image):

    results = model(image)

    faces = []

    for r in results:

        boxes = r.boxes.xyxy.cpu().numpy()

        for box in boxes:

            x1, y1, x2, y2 = map(int, box)

            faces.append((x1, y1, x2, y2))

    return faces
```
