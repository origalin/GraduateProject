import cv2
import numpy as np

img = cv2.imread("D:\\USB2_CMOS_5M_YM@CC505000042 20140704164935.bmp")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
y = cv2.Sobel(img, cv2.CV_16S, 0, 1)

absX = cv2.convertScaleAbs(x)  # 转回uint8
absY = cv2.convertScaleAbs(y)
dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
cv2.namedWindow('Result1', cv2.WINDOW_FREERATIO)
cv2.namedWindow('Result2', cv2.WINDOW_FREERATIO)
cv2.namedWindow('Result', cv2.WINDOW_FREERATIO)
cv2.namedWindow('Open', cv2.WINDOW_FREERATIO)
cv2.namedWindow('Close', cv2.WINDOW_FREERATIO)
cv2.imshow("Result1", dst)

cv2.threshold(dst, 36, 255, cv2.THRESH_BINARY, dst)

cv2.imshow("Result", dst)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# 开运算
open = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
# 显示腐蚀后的图像
cv2.imshow("Open", open)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
# 闭运算
closed = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)
# 显示腐蚀后的图像
cv2.imshow("Close", closed)

image, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 0, 255), 1)
cv2.imshow("Result2", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
