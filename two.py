# 学校：广东海洋大学
# 学生：赵俊豪
# 开发时间：2022/10/30 20:53
# coding:utf-8
from collections import deque
import numpy as np
import time
import cv2

# 设定红色阈值，HSV空间
redLower = np.array([170, 100, 100])
redUpper = np.array([179, 255, 255])
greenLower = np.array([35, 43, 46])
greenUpper = np.array([77, 255, 255])
# 打开摄像头
camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# 等待两秒
# time.sleep(3)
# 遍历每一帧，检测红色识别物体
while True:
    # 读取帧
    (ret, frame) = camera.read()
    # 判断是否成功打开摄像头
    if not ret:
        print
        'No Camera'
        break
    # frame = imutils.resize(frame, width=600)
    # 转到HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 根据阈值构建掩膜，也就是黑白图像
    red_mask = cv2.inRange(hsv, redLower, redUpper)
    green_mask = cv2.inRange(hsv, greenLower, greenUpper)
    # 腐蚀操作
    red_mask = cv2.erode(red_mask, None, iterations=2)
    green_mask = cv2.erode(green_mask, None, iterations=2)
    # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    red_mask = cv2.dilate(red_mask, None, iterations=2)
    cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    green_mask = cv2.dilate(green_mask, None, iterations=2)
    cnts2 = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 如果存在轮廓
    if len(cnts) > 0:
        # 找到面积最大的轮廓
        c = max(cnts, key=cv2.contourArea)
        # 确定面积最大的轮廓的外接圆
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        ##其实这里就结束了#################
        # 只有当半径大于10时，才执行画图
        if radius > 10:
            print((x,y),'radius:%d' % radius)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
    if len(cnts2) > 0:
        # 找到面积最大的轮廓
        c2 = max(cnts2, key=cv2.contourArea)
        # 确定面积最大的轮廓的外接圆
        ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
        ##其实这里就结束了#################
        # 只有当半径大于10时，才执行画图
        if radius2 > 10:
            print((x2,y2),'radius:%d' % radius2)
            cv2.circle(frame, (int(x2), int(y2)), int(radius2), (0, 255, 255), 2)

    cv2.imshow('Frame', frame)
    # 键盘检测，检测到esc键退出
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
# 摄像头释放
camera.release()
# 销毁所有窗口
cv2.destroyAllWindows()