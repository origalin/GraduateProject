import cv2
import numpy as np


def getMarkedImage(filename):
    origin = cv2.imread(filename)
    img = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)

    dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 1)
    # cv2.imshow("TrResult", dst)

    cv2.threshold(dst, 20, 255, cv2.THRESH_BINARY_INV, dst)
    # cv2.imshow("Result", dst)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # 开运算
    opend = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("Open", opend)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    # 闭运算
    closed = cv2.morphologyEx(opend, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Close", closed)

    image, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    redFree = cv2.merge([origin[:, :, 0], origin[:, :, 1], np.zeros((origin.shape[0], origin.shape[1]), np.uint8)])
    h, w, _ = origin.shape
    redTmp = np.zeros(origin.shape, np.uint8)
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > (h / 20 * w / 20):
            c_min = [cnt]
            cv2.drawContours(redTmp, c_min, -1, (0, 0, 255), -1)
    result = cv2.addWeighted(redFree, 1, redTmp, 1, 0.0)
    cv2.imshow("Result", result)
    return result


def analyseImage(img):
    red = img[:, :, 2]
    simpleImage = cv2.merge([red])
    image, contours, hierarchy = cv2.findContours(simpleImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    f = open("output.txt", 'w')
    for i in range(len(contours)):
        (x, y), (MA, ma), angle = cv2.fitEllipse(contours[i])
        x = int(x)
        y = int(y)
        MA = int(MA)
        ma = int(ma)
        f.write("position:(%d, %d),length: %d,width: %d\r\n" % (x, y, MA, ma))
    f.close()
    cv2.imshow("Image", simpleImage)
