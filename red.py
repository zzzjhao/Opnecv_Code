# 学校：广东海洋大学
# 学生：赵俊豪
# 开发时间：2022/10/30 20:28
def green_point_video(frame):
    kernel_2 = np.ones((2, 2), np.uint8)  # 2x2的卷积核
    kernel_3 = np.ones((3, 3), np.uint8)  # 3x3的卷积核
    kernel_4 = np.ones((4, 4), np.uint8)  # 4x4的卷积核
    kernel_8 = np.ones((8, 8), np.uint8)
    Lower_red = np.array([156, 128, 46])
    Upper_red = np.array([180, 255, 255])
    red = [Lower_red, Upper_red, 'red']
    Lower_white = np.array([0, 0, 200])  # 221
    Upper_white = np.array([180, 30, 255])
    white = [Lower_white, Upper_white, 'white']
    Lower_black = np.array([0, 0, 0])
    Upper_black = np.array([180, 255, 46])
    black = [Lower_black, Upper_black, 'black']
    Lower_green = np.array([35, 95, 46])
    Upper_green = np.array([70, 255, 255])
    green = [Lower_green, Upper_green, 'green']
    Lower_blue = np.array([80, 80, 150])
    Upper_blue = np.array([110, 255, 255])
    blue = [Lower_blue, Upper_blue, 'blue']
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
    color = green
    if color[2] == 'green':
        mask_red = cv2.inRange(HSV, color[0], color[1])
        erosion = cv2.erode(mask_red, kernel_2, iterations=1)
        erosion = cv2.erode(erosion, kernel_4, iterations=1)
        erosion = cv2.erode(erosion, kernel_4, iterations=1)
        dilation = cv2.dilate(erosion, kernel_2, iterations=1)
        dilation = cv2.dilate(dilation, kernel_4, iterations=1)
        dilation = cv2.dilate(dilation, kernel_8, iterations=1)
        ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)  # 二值化，将滤波后的图像变成二值图像放在binary中
        cnts = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)  # 寻找轮廓
        green_list = []
        for c in cnts:
            # compute the center of the contour
            M0 = cv2.moments(c)
            # cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            car_video_location = [int(M0["m10"] / M0["m00"]), int(M0["m01"] / M0["m00"])]
            cv2.circle(frame, (car_video_location[0], car_video_location[1]), 7, (0, 255, 0), -1)
            cv2.putText(frame, "green", (car_video_location[0] - 20, car_video_location[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.imshow("Image", frame)
            green_point = [int(M0["m10"] / M0["m00"]), int(M0["m01"] / M0["m00"])]
            green_list = green_list + green_point
        # if len(green_list) == 6:  # 起始可能识别不到3个红色块，等都识别到，再输出坐标
        #     print('红色块1', green_list[0], green_list[1])
        #     print('红色块2', green_list[2], green_list[3])
        #     print('红色块3', green_list[4], green_list[5])
    return green_list


def red_point_video(frame):
    kernel_2 = np.ones((2, 2), np.uint8)  # 2x2的卷积核
    kernel_3 = np.ones((3, 3), np.uint8)  # 3x3的卷积核
    kernel_4 = np.ones((4, 4), np.uint8)  # 4x4的卷积核
    kernel_8 = np.ones((8, 8), np.uint8)
    Lower_red = np.array([156, 128, 46])
    Upper_red = np.array([180, 255, 255])
    red = [Lower_red, Upper_red, 'red']
    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
    color = red
    mask_red = cv2.inRange(HSV, color[0], color[1])
    erosion = cv2.erode(mask_red, kernel_2, iterations=1)
    erosion = cv2.erode(erosion, kernel_4, iterations=1)
    erosion = cv2.erode(erosion, kernel_4, iterations=1)
    dilation = cv2.dilate(erosion, kernel_2, iterations=1)
    dilation = cv2.dilate(dilation, kernel_4, iterations=1)
    dilation = cv2.dilate(dilation, kernel_8, iterations=1)
    ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)  # 二值化，将滤波后的图像变成二值图像放在binary中
    cnts = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    red_list = []
    for c in cnts:
        # compute the center of the contour
        M0_red = cv2.moments(c)

        # cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        car_video_location = [int(M0_red["m10"] / M0_red["m00"]), int(M0_red["m01"] / M0_red["m00"])]
        cv2.circle(frame, (car_video_location[0], car_video_location[1]), 7, (0, 0, 255), -1)
        cv2.putText(frame, "red", (car_video_location[0] - 20, car_video_location[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Image", frame)
        red_point = [int(M0_red["m10"] / M0_red["m00"]), int(M0_red["m01"] / M0_red["m00"])]
        # red_point = [int(M0["m10"] / M0["m00"]), int(M0["m01"] / M0["m00"])
        red_list = red_list + red_point
    # print('红色', red_list)
    # if len(red_list) == 6:  # 起始可能识别不到3个红色块，等都识别到，再输出坐标
    #     print('红色块1', red_list[0], red_list[1])
    #     print('红色块2', red_list[2], red_list[3])
    #     print('红色块3', red_list[4], red_list[5])
    return red_list



#  主函数：识别红色和绿色并在输出视频实时显示标记中心
import cv2
import numpy as np
import imutils

if __name__ == "__main__":
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        ret, sframe = cap.read()
        green_video_point = green_point_video(sframe)  # 绿色点在视频中的坐标，并在输出标记
        green_video_point = red_point_video(sframe)
        cv2.imshow("Image", sframe)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.waitKey(300)  # 延时30msq