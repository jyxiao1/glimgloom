# import the necessary packages
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        # print(c)
        # approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if (4000 < area < 4500) and (250 < peri < 260):
            shape = "hexagon"
            return shape
        if (area > 15000) and (400 < peri < 800):
            print(str(peri) + " " + str(area))
            shape = "rectangle"

        return shape
