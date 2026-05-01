```python
import cv2

def beauty_filter(img):

    smooth = cv2.bilateralFilter(
        img,
        15,
        75,
        75
    )

    bright = cv2.convertScaleAbs(
        smooth,
        alpha=1.1,
        beta=8
    )

    return bright
```
