import cv2 as cv
import numpy as np
import math
import os
def line_detection(image):
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray,50,150,apertureSize=3)    #apertureSize是sobel算子大小，只能为1,3,5，7
    lines = cv.HoughLines(edges,1,np.pi/180,200)  #函数将通过步长为1的半径和步长为π/180的角来搜索所有可能的直线
    for line in lines:
        rho,theta = line[0]#获取极值ρ长度和θ角度
        a = np.cos(theta)#获取角度cos值
        b = np.sin(theta)#获取角度sin值
        x0 = a * rho#获取x轴值
        y0 = b * rho#获取y轴值　　x0和y0是直线的中点
        x1 = int(x0 + 1000*(-b))#获取这条直线最大值点x1
        y1 = int(y0 + 1000*(a))#获取这条直线最大值点y1
        x2 = int(x0 - 1000 * (-b))#获取这条直线最小值点x2　　
        y2 = int(y0 - 1000 * (a))#获取这条直线最小值点y2　　其中*1000是内部规则
        cv.line(image,(x1,y1),(x2,y2),(0,0,255),2)#开始划线
    cv.imshow("image line",image)

def line_detect_possible_demo(image,image2,im_name):
    len=[]
    #len.append(im_name)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)  # apertureSize是sobel算子大小，只能为1,3,5，7
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50,maxLineGap=60)  #函数将通过步长为1的半径和步长为π/180的角来搜索所有可能的直线
    for line in lines:
        x1,y1,x2,y2 = line[0]
        if 1>0:

            #print(type(line))   #多维数组
            
            len.append(math.sqrt((y2-y1)*(y2-y1)+(x2-x1)*(x2-x1)).__str__())
        
            cv.line(image,(x1,y1),(x2,y2),(0,0,255),2)
            cv.line(image2,(x1,y1),(x2,y2),(0,0,255),2)
    cv.imwrite("/media/autolab/disk_3T/line/"+im_name,image)
    cv.imwrite("/media/autolab/disk_3T/line2/"+im_name,image2)
    len.sort()
    len.reverse()
    return len



dir_path = '/media/autolab/disk_3T/highway_binary/'
image_name_list=os.listdir(dir_path)
image_name_list.sort()

dir_path2 = '/media/autolab/disk_3T/highway_changed/'
image_name_list2=os.listdir(dir_path2)
image_name_list2.sort()

lens=[]
for i in range(0,len(image_name_list)):
    src = cv.imread("/media/autolab/disk_3T/highway_binary/"+image_name_list[i])#读取图片
    src2 = cv.imread("/media/autolab/disk_3T/highway_changed/"+image_name_list2[i])#读取图片
    lens.append(line_detect_possible_demo(src,src2,image_name_list[i]))


#line_detection(src)

filename='/media/autolab/disk_3T/length.txt'
with open(filename,'w') as f: 
    for i in range(0,len(lens)):
        #for j in range(0,len(lens[i])):
        f.write(lens[i][0].__str__()+' ')
            #print(lens[i][j])
        f.write('\n')
        #f.write('\n')
   