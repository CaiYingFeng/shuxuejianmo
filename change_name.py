import os



dir_path = '/media/autolab/disk_3T/highway/'

image_name_list=os.listdir(dir_path)
image_path_list=[os.path.join(dir_path,image_name)for image_name in image_name_list]
image_path_list.sort()
for image_name in image_path_list:

    
    os.rename(image_name,image_name[:37]+'png')