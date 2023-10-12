# 学校：广东海洋大学
# 学生：赵俊豪
# 开发时间：2022/11/1 20:20
import cv2
import numpy as np

# capturing video through webcam

#cap= cv2.VideoCapture(0,cv2.CAP_DSHOW)

#cap.set(1, 1)#摄像头/视频-亮度调节
#cap = cv2.VideoCapture("Sample_Video.mp4")
#cap = cv2.VideoCapture("trafficlight.mp4")
cap = cv2.VideoCapture("rld.mp4")

while (1):
    _, img = cap.read()

    # converting frame(img == BGR) to HSV(hue-saturation-value)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # red color
    '''red_lower = np.array([0,95,230],np.uint8)  r:136       #这两个是阈值，红灯的上界和下界
    red_upper = np.array([5,255,255], np.uint8)'''

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # green color，35, 43, 35
    # greenLower = np.array([35, 43, 46])
    #green_lower = np.array([136, 43, 35], np.uint8)'''1'''
    #greenUpper = np.array([77, 255, 255])
    #green_upper = np.array([77, 255, 255], np.uint8)
    #lower_green = np.array([40,50,50])/upper_green = np.array([90,255,255])
    green_lower = np.array([40,50,50])
    green_upper = np.array([90,255,255])

    # yellow color
    #[26,43,46],[34,255,255]
    '''yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)'''
    '''yellow_lower = np.array([120,65,46], np.uint8)
    yellow_upper = np.array([34, 255, 255], np.uint8)'''
    yellow_lower = np.array([15, 150, 150])
    yellow_upper = np.array([35, 255, 255])

    # all color together
    red = cv2.inRange(hsv, red_lower, red_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Morphological Transform, Dilation
    kernal = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernal)
    res_red = cv2.bitwise_and(img, img, mask=red)

    green = cv2.dilate(green, kernal)
    res_green = cv2.bitwise_and(img, img, mask=green)

    yellow = cv2.dilate(yellow, kernal)
    res_yellow = cv2.bitwise_and(img, img, mask=yellow)

    # Tracking red
    contours, hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Red light", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

    # Tracking green
    contours, hierarchy = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Green light", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))

    # Tracking yellow
    contours, hierarchy = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,255), 2)
            cv2.putText(img, "Yellow light", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (50, 200, 200))



    cv2.imshow("Color Tracking", img)
    if cv2.waitKey(10) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        break