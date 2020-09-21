import cv2  
import numpy as np    
  
img = cv2.imread("/media/autolab/disk_3T/highway_binary/00002.bmp", 0)  
  
x = cv2.Sobel(img,cv2.CV_16S,1,0)  
y = cv2.Sobel(img,cv2.CV_16S,0,1)  
  
absX = cv2.convertScaleAbs(x)   # 转回uint8  
absY = cv2.convertScaleAbs(y)  
  
dst = cv2.addWeighted(absX,0.5,absY,0.5,0)  
  
# cv2.imshow("absX", absX)  
# cv2.imshow("absY", absY)  
  
for i in range(0,len(dst)):
    for j in range(0,len(dst[i])):
        if dst[i][j]==255:
            dst[i][j]=0
        else:
            dst[i][j]=255
cv2.imwrite("Result.png", dst)  
  
# # cv2.waitKey(0)  
# # cv2.destroyAllWindows()   

# from skimage import data,filters
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg # mpimg 用于读取图片
# img = mpimg.imread('/media/autolab/disk_3T/highway_binary/00002.bmp')
# edges = filters.prewitt(img)
# plt.imsave("prewitt.png",edges)

# edges = filters.roberts(img)
# cv2.imwrite("robert.png", edges)