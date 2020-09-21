#相关包
import numpy as np
import cv2
import imutils
import time
import matplotlib.pyplot as plt
from PIL import *
# from tensorflow.keras.preprocessing.image import img_to_array,array_to_img
from skimage.filters import threshold_local

#image = cv2.imdecode(np.fromfile(r"/media/autolab/disk_3T/Math/haze/original_frame95.bmp"),-1)
image = cv2.imread("original_frame95.bmp")
print(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ratio = image.shape[0] / 500
# print("ratio:",ratio)
orig = image.copy()
#调整图像的大小
image = imutils.resize(image,height=500)

print("改变之后的image:",image.shape)

#对图像进行灰度图处理，然后在进行高斯模糊滤波处理（去除非椒盐噪声）
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray)
gray = cv2.GaussianBlur(gray, (3,3), 0)
print("gray.shape:",gray.shape)
# it=time.time()
# for i in range(256):
# for j in range(i+1):
#进行边缘处理，一种是阈值处理，一种是自动边缘处理
edged1 = imutils.auto_canny(gray,sigma=3)
edged = cv2.Canny(gray,170, 200)
edged1 = cv2.dilate(edged1, None)

cv2.imshow("Edged and edged1",edged)
cv2.imshow("Edged aed1",edged1)
cv2.imshow("edged and edged1",np.hstack([edged,edged1]))
cv2.waitKey(0)
cv2.destroyAllWindows()

#这里的操作和上个学习笔记4的一样，不做介绍
def order_points(pts):
    #进行初始化点的位置，左上、右上、左下、右下
    rect = np.zeros((4, 2), dtype = "float32")
    #采取四个点的x+y的和，以最小的和为左上的点，x+y最大为右下的点
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
   #定义一左下点和右上点的位置，用|x-y|表示，小的为右上，大的为左下
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect
def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    #重新计算新的图像的宽度和高度
    widthA = np.sqrt(np.sum((br - bl) ** 2))
    widthB = np.sqrt(np.sum((tr - tl) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(np.sum((tr - br) ** 2))
    heightB = np.sqrt(np.sum((tl - bl) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    #重新定义新的图像的四边顶点的坐标
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # 计算透视矩阵，并且变化应用
    M = cv2.getPerspectiveTransform(rect, dst)
    print(M)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped

#发现轮廓，并且用imutils.grab_contours()函数返回轮廓
cnts = cv2.findContours(edged1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print(cnts)
#这一步是进行轮廓所围成的面积，并且进行从大到小的排列
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
for c in cnts:
   
    #获取轮廓的周长
    peri = cv2.arcLength(c, True)
    #用该函数进行图形的相似
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    #如果我们相似的轮廓是四个点表示的，那么我们就可以看作这是轮廓点就是我们所要的
    if len(approx) == 4:
        screenCnt = approx
        break
    print(screenCnt)

    
#画出轮廓
cv2.drawContours(image, [screenCnt], -1, (0, 255, 255), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


#进行透视转换
warped = four_point_transform(orig, screenCnt.reshape(4, 2)*ratio)
#把彩色图像进行灰度处理，然后对其进行黑白化处理
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
#将灰度图像变成黑白纸的形式
T = threshold_local(warped, 11, offset = 9, method = "gaussian")
warped = (warped > T).astype("uint8") * 255


cv2.imshow("Original", imutils.resize(orig, height = 500))
cv2.imshow("Scanned", imutils.resize(warped, height = 500))
#cv2.imshow("and",np.hstack([cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY),warped]))
cv2.waitKey(0)


