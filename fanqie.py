# 学校：广东海洋大学
# 学生：赵俊豪
# 开发时间：2022/10/30 23:25
import cv2
import numpy as np

#cap = cv2.VideoCapture("D:/python/.idea/inspectionProfiles/lanwang/trafficlight.mp4")
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#cap = cv2.VideoCapture("Sample_Video.mp4")
cap = cv2.VideoCapture("rld.mp4")
#cap.set(5,1)


while True:
    ret,frame = cap.read()
    if ret == False:
        break
    frame = cv2.resize(frame,(1920,1080))
    #截取roi区域
    roiColor = frame[0:2000,0:1800]
    #转换hsv颜色空间
    hsv = cv2.cvtColor(roiColor,cv2.COLOR_BGR2HSV)

    #red
    lower_hsv_red = np.array([160,177,122])
    upper_hsv_red = np.array([179,255,255])
    mask_red = cv2.inRange(hsv,lowerb=lower_hsv_red,upperb=upper_hsv_red)
    #中值滤波
    red_blur = cv2.medianBlur(mask_red, 7)
    #green
    lower_hsv_green = np.array([60,79,137])
    upper_hsv_green = np.array([90,255,255])
    mask_green = cv2.inRange(hsv,lowerb=lower_hsv_green,upperb=upper_hsv_green)
    #中值滤波
    green_blur = cv2.medianBlur(mask_green, 7)

    #因为图像是二值的图像，所以如果图像出现白点，也就是255，那么就取他的max最大值255
    red_color = np.max(red_blur)
    green_color = np.max(green_blur)
    #在red_color中判断二值图像如果数值等于255，那么就判定为red
    if red_color == 255:
        print('red')
                        #。。。这是我经常会混淆的坐标。。。 就列举出来记一下。。。
                        #      y  y+h x  x+w
                        #frame[50:90,950:1100]

                        #     x   y    x+w  y+h
        cv2.rectangle(frame,(1020,50),(1060,90),(0,0,255),2) #按坐标画出矩形框
        cv2.putText(frame, "red", (1020, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255),2)#显示red文本信息
    #在green_color中判断二值图像如果数值等于255，那么就判定为green
    elif green_color == 255:
        print('green')
        cv2.rectangle(frame,(1020,50),(1060,90),(0,255,0),2)
        cv2.putText(frame, "green", (1020, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),2)

    cv2.imshow('frame',frame)
    red_blur = cv2.resize(red_blur,(300,200))
    green_blur = cv2.resize(green_blur,(300,200))
    cv2.imshow('red_window',red_blur)
    cv2.imshow('green_window',green_blur)

    c = cv2.waitKey(100)
    if c==27:
        break
