import cv2
import numpy as np
import os

def change_view(im_name):
    impath='/media/autolab/disk_3T/highway/'+im_name
    # 读取名称为 p19.jpg的图片
    img = cv2.imread(impath,1)
    img_org = cv2.imread(impath,1)

    # 得到图片的高和宽
    img_height,img_width = img.shape[:2]

    # 定义对应的点
    #points1 = np.float32([[391,505], [445,471], [479,715], [591,659]])#原始
    #points2 = np.float32([[391,505], [445,471], [503,709], [560,676]])#变后

    points1 = np.float32([[405,537], [529,480], [482,719], [688,627]])#前
    points2 = np.float32([[405,537], [529,480], [498,713], [627,655]])#后


    # 计算得到转换矩阵
    M = cv2.getPerspectiveTransform(points1, points2)

    # 实现透视变换转换
    processed = cv2.warpPerspective(img,M,(1280, 720))

    # 显示原图和处理后的图像
    
    cv2.imwrite('/media/autolab/disk_3T/highway_changed/'+im_name,processed)

    return M

dir_path = '/media/autolab/disk_3T/highway/'

image_name_list=os.listdir(dir_path)
image_name_list.sort()
# image_path_list=[os.path.join(dir_path,image_name)for image_name in image_name_list]
# image_path_list.sort()

for i in range(0,1):
    
    M=change_view(image_name_list[i])
    for i in range(0,3):
        for j in range(0,3):
            print(M[i][j])
        print('\n')
    

