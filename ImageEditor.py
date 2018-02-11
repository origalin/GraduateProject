import cv2
import numpy as np

# 当鼠标按下时设置 要进行绘画
drawing = False
finished = False
pre_x = 0
pre_y = 0
thickness = 5
reverse = 0
img = []


def blankcallback(position):
    global thickness
    thickness = position
    print('滚动条当前位置为%d' % position)

def reversecallback(position):
    global reverse
    reverse = position

def onfinish(position):
    global finished
    finished = True

# 创建回调函数，用于设置滚动条的位置
def drawcircle(event, x, y, flags, param):
    color = (0, 0, 255)

    global drawing, pre_x, pre_y, thickness, reverse

    # 当按下左键时，返回起始的位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pre_x = x
        pre_y = y
    # 当鼠标左键按下并移动则是绘画圆形，event可以查看移动，flag查看是否按下
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing:
            drawTranceLine(img, pre_x, pre_y, x, y, color, thickness, reverse)
            pre_x = x
            pre_y = y
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False


def drawTranceLine(img, s_x, s_y, e_x, e_y, color, thickness, reverse):
    rec = np.zeros(img.shape, np.uint8)
    cv2.line(rec, (s_x, s_y), (e_x, e_y), color, thickness)
    width = abs(s_x - e_x) + 2 * thickness
    height = abs(s_y - e_y) + 2 * thickness
    start_x = int((s_x + e_x) / 2 - width / 2)
    start_y = int((s_y + e_y) / 2 - height / 2)
    if start_x < 0:
        start_x = 0
    if start_y < 0:
        start_y = 0
    roi = img[start_y:start_y + height, start_x:start_x + width]
    roi2 = rec[start_y:start_y + height, start_x:start_x + width]
    if reverse:
        cv2.addWeighted(roi, 1, roi2, -1, 0.0, roi)
    else:
        cv2.addWeighted(roi, 1, roi2, 1, 0.0, roi)
    img[start_y:start_y + height, start_x:start_x + width] = roi


def editImage(img_in):
    global img, finished
    img = img_in
    cv2.namedWindow('EditImage', cv2.WINDOW_FREERATIO)
    cv2.setMouseCallback('EditImage', drawcircle)
    cv2.createTrackbar('Thickness', 'EditImage', 0, 100, blankcallback)
    cv2.createTrackbar('Reverse', 'EditImage', 0, 1, reversecallback)
    cv2.createTrackbar('Confirm', 'EditImage', 0, 1, onfinish)
    cv2.setTrackbarPos('Thickness', 'EditImage', 5)

    while True:
        cv2.imshow('EditImage', img)
        key = cv2.waitKey(10) & 0xFFF
        if key == 27 or finished:
            break
    return img
