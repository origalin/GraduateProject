import cv2
import numpy as np


def getMarkedImage(filename):
    origin = cv2.imread(filename)
    img = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)

    dst = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 0)
    # cv2.namedWindow('TrResult', cv2.WINDOW_FREERATIO)
    # cv2.namedWindow('Open', cv2.WINDOW_FREERATIO)
    # cv2.namedWindow('Close', cv2.WINDOW_FREERATIO)
    # cv2.namedWindow('Result', cv2.WINDOW_FREERATIO)
    # cv2.imshow("TrResult", dst)

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
    # cv2.imshow("Result", redTmp)
    return result


def analyseImage(img):
    h, w, _ = img.shape
    red = img[:, :, 2]
    simpleImage = cv2.merge([red])
    image, contours, hierarchy = cv2.findContours(simpleImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    data = ""
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > (h / 20 * w / 20):
            (x, y), (MA, ma), angle = cv2.fitEllipse(contours[i])
            x = int(x)
            y = int(y)
            MA = int(MA)
            ma = int(ma)
            data += "position:(%d, %d),length: %d,width: %d\r\n" % (x, y, ma, MA)
            cv2.putText(img, "(%d %d)" % (ma, MA), (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0))
            cv2.drawContours(img, [contours[i]], -1, (0, 0, 0), 1)
            # cv2.imshow("Image", img)
    return data
