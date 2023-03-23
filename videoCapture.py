# -*- coding: utf-8 -*
import cv2
import numpy as np

# 创建一个video capture的实例
# VideCapture里面的序号
# 0 : 默认为笔记本上的摄像头(如果有的话) / USB摄像头 webcam
# 1 : USB摄像头2
# 2 ：USB摄像头3 以此类推
# -1：代表最新插入的USB设备
cap = cv2.VideoCapture(0)

# 查看Video Capture是否已经打开
print("摄像头是否已经打开 ？ {}".format(cap.isOpened()))
width = 640
height = 480
# 设置画面的尺寸
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 创建一个名字叫做 “image_win” 的窗口
# 窗口属性 flags
#   * WINDOW_NORMAL：窗口可以放缩
#   * WINDOW_KEEPRATIO：窗口缩放的过程中保持比率
#   * WINDOW_GUI_EXPANDED： 使用新版本功能增强的GUI窗口
cv2.namedWindow('src_image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
cv2.resizeWindow('src_image', int(width), height)

# 图像计数 从1开始
img_count = 1

while True:
    # 获取图像，如果画面读取成功 ret=True，frame是读取到的图片对象(numpy的ndarray格式)
    ret, frame = cap.read()
    if not ret:
        print("图像获取失败，请按照说明进行问题排查")
        # 读取失败？问题排查
        print("* 硬件问题     \t在就是检查一下USB线跟电脑USB接口")
        print("* 设备挂载问题  \t摄像头没有被挂载，如果是虚拟机需要手动勾选设备")
        print("* 接口兼容性问题\t或者USB2.0接口接了一个USB3.0的摄像头，也是不支持的。")
        print("* 驱动问题     \t有的摄像头可能存在驱动问题，需要安装相关驱动，或者查看摄像头是否有UVC免驱协议")
        break

    cv2.imshow('src_image', frame)
    # 等待按键事件发生 单位毫秒
    key = cv2.waitKey(2)
    if key == ord('q'):
        print("程序退出...")
        break
    elif key == ord('c'):
        # 如果c键按下，则进行图片保存
        # 写入图片 并命名图片为 图片序号.png
        cv2.imwrite("{}.png".format(img_count), frame)
        print("保存图片为  {}.png".format(img_count))
        # 图片编号计数自增1
        img_count += 1
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        cv2.imshow('src_image', frame)
        key = cv2.waitKey(2)
    # 将BGR彩图变换为灰度图
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray_image', gray_frame)

    # 二值化显示
    (thresh, gray) = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('threshold_image', gray)

    # 图片镜像
    # 水平翻转 flipCode = 1
    # 垂直翻转 flipCode = 0
    # 同时水平翻转与垂直翻转 flipCode = -1
    flipCode = -1
    flip_frame = cv2.flip(frame, flipCode)
    cv2.imshow('flip_image', flip_frame)

# 释放VideoCapture
cap.release()
# 销毁所有的窗口
cv2.destroyAllWindows()
