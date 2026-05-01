```python
from tensorflow.keras.models import load_model
import cv2
import numpy as np

acne_model = load_model("models/acne_model.h5")

classes = [
    "Clear",
    "Mild",
    "Moderate",
    "Severe"
]

def predict_acne(face):

    img = cv2.resize(face, (224,224))

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    pred = acne_model.predict(img)[0]

    idx = np.argmax(pred)

    label = classes[idx]

    confidence = round(float(pred[idx]) * 100, 2)

    return label, confidence
```
