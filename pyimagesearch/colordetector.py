# import the necessary packages
import cv2
import numpy as np

class ColorDetector:
    def __init__(self):
        pass

    def determine_color(self, image, c):
        color = "unidentified"
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        # mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        if (70 < mean[0] < 90) and (50 < mean[1] < 70) and (90 < mean[2] < 110):
            color = "black"
        else:
            color = "white"
        return color