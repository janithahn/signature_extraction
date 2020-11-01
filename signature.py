import numpy as np
import cv2
import matplotlib.pyplot as plt

# image = cv2.imread('output/img_cropped1.jpg')
image = cv2.imread('input/in8.jpg')
result = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([90, 38, 0])
upper = np.array([145, 255, 255])
mask = cv2.inRange(image, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

#cv2.imshow('mask', mask)
#cv2.imshow('close', close)

plt.imshow(mask)
plt.title('mask')
plt.axis('off')
plt.show()

plt.imshow(close)
plt.title('close')
plt.axis('off')
plt.show()

cv2.waitKey()
