import cv2
import matplotlib.pyplot as plt

image = cv2.imread("/mnt/c/Users/Rahul/Desktop/Docs and Essentials/Confidential Passports/hajurba.JPG", 0)

th, res = cv2.threshold(image, 130, 255, cv2.THRESH_BINARY)

# Use matplotlib to display the image
plt.imshow(res, cmap='gray')
plt.title("Thresholded Image")
plt.axis('off')
plt.show()
