import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
img = cv.imread('/media/autolab/disk_3T/highway_binary/00002.bmp', cv.COLOR_BGR2GRAY)
# rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# 灰度化处理图像
grayImage = img

# Prewitt 算子
kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],dtype=int)
kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=int)

x = cv.filter2D(grayImage, cv.CV_16S, kernelx)
y = cv.filter2D(grayImage, cv.CV_16S, kernely)

# 转 uint8 ,图像融合
absX = cv.convertScaleAbs(x)
absY = cv.convertScaleAbs(y)
Prewitt = cv.addWeighted(absX, 0.5, absY, 0.5, 0)

Roberts=Prewitt

for i in range(0,len(Roberts)):
    for j in range(0,len(Roberts[i])):
        if Roberts[i][j]==255:
            Roberts[i][j]=0
        else:
            Roberts[i][j]=255

cv.imwrite("Prewitt.png", Roberts)  