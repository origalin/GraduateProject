import cv2
import numpy as np


def blankcallback(position):
    print('value %d' % position)

# 当鼠标按下时设置 要进行绘画
drawing = False

# 如果mode为True时就画矩形，按下‘m'变为绘制曲线
mode = True


# globalx, globaly = -1,-1

# 创建回调函数，用于设置滚动条的位置
def drawcircle(event, x, y, flags, param):
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    color = (b, g, r, 0.1)

    global globalx, globaly, drawing, mode, pre_x, pre_y

    # 当按下左键时，返回起始的位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pre_x = x
        pre_y = y
        # globaly,globaly = x,y
    # 当鼠标左键按下并移动则是绘画圆形，event可以查看移动，flag查看是否按下
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing == True:
            if mode == True:
                # cv2.line(img, (pre_x, pre_y), (x, y), color, 30)
                drawTranceLine(img, pre_x, pre_y, x, y, color, 30)
                pre_x = x
                pre_y = y
            else:
                # 绘制圆圈，小圆点连接在一起成为线，1代表了比划的粗细
                cv2.circle(img, (x, y), 16, color, 32)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False


def drawTranceLine(img, s_x, s_y, e_x, e_y, color, thickness):
    rec = np.zeros(img.shape, np.uint8)
    cv2.line(rec, (s_x, s_y), (e_x, e_y), color, thickness)
    width = abs(s_x - e_x) + 2 * thickness
    height = abs(s_y - e_y) + 2 * thickness
    start_x = int((s_x + e_x) / 2 - width / 2)
    start_y = int((s_y + e_y) / 2 - height / 2)
    roi = img[start_y:start_y + height, start_x:start_x + width]
    roi2 = rec[start_y:start_y + height, start_x:start_x + width]
    cv2.addWeighted(roi, 1, roi2, 1, 0.0, roi)
    img[start_y:start_y + height, start_x:start_x + width] = roi
    print(start_y)


img = cv2.imread('D:\\img\\USB2_CMOS_5M_YM@CC505000042 20140704164935.bmp')
cv2.namedWindow('image', cv2.WINDOW_FREERATIO)

cv2.createTrackbar('R', 'image', 0, 255, blankcallback)
cv2.createTrackbar('G', 'image', 0, 255, blankcallback)
cv2.createTrackbar('B', 'image', 0, 255, blankcallback)
cv2.setMouseCallback('image', drawcircle)

while True:
    cv2.imshow('image', img)

    key = cv2.waitKey(10) & 0xFFF
    if key == 27:
        break

cv2.destroyAllWindows()
