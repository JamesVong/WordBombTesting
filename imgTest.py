import cv2
import numpy as np


def test_image(img):
    img = cv2.resize(img, None, fx=3, fy=3)
    cv2.imwrite('img.png', img)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Mask
    lower = np.array([110, 139, 0])
    upper = np.array([360, 255, 60])
    mask = cv2.inRange(img_hsv, lower, upper)

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask == 0)] = 255
    output_img[np.where(mask != 0)] = 0

    cv2.imwrite('mask.png', output_img)
    return output_img

