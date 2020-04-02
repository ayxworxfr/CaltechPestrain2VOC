#-*- coding:utf-8 -*-
import os
import glob
import shutil
if __name__ == "__main__":
    imgpathin = 'D:/BaiduYunDownload/CaltechPestrain2VOC/jpg'
    imgout = 'D:/BaiduYunDownload/CaltechPestrain2VOC/newjpg'
    for subdir in os.listdir(imgpathin):
        print (subdir)
        file_path = os.path.join(imgpathin,subdir)
        for subdir1 in os.listdir(file_path):
            print (subdir1)
            #jpg_files = glob.glob(os.path.join(file_path, subdir1, "*.jpg"))
            file_path1 = os.path.join(file_path, subdir1)
            for jpg_file in os.listdir(file_path1):
                #print jpg_file
 
                src = os.path.join(file_path1, jpg_file)
                new_name=str(subdir+"_"+subdir1+"_"+jpg_file)
                dst=os.path.join(imgout,new_name)
                os.rename(src,dst)
