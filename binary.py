import cv2
import numpy as np
import os


# 全局阈值
def threshold_demo(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ret, binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    ret, binary = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    print("阈值：", ret)
    cv2.imwrite("binar1y.jpg", binary)


# 局部阈值
def local_threshold(image,im_name):
    gray = cv2.cvtColor(image,cv2.COLOR_BGRA2GRAY)
    binary1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,2)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15, 2)
    cv2.imwrite('/media/autolab/disk_3T/highway_binary/'+im_name, binary)
    cv2.imwrite("binary21.jpg", binary1)



def custom_threshold(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGRA2GRAY)
    h, w = gray.shape[:2]
    m = np.reshape(gray, [1, w*h])
    mean = m.sum()/(w*h)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,25,10)
    ret, binary = cv2.threshold(gray, mean, 255, cv2.THRESH_BINARY)
    cv2.imwrite("binary3.jpg", binary)




dir_path='/media/autolab/disk_3T/highway_changed/'

image_name_list=os.listdir(dir_path)
image_name_list.sort()


for i in range(0,len(image_name_list)):
    
    img = cv2.imread('/media/autolab/disk_3T/highway_changed/'+image_name_list[i])
    #threshold_demo(img)
    local_threshold(img,image_name_list[i])
    #custom_threshold(img)
    #cv2.waitKey(0)