# -*- coding:utf-8 -*-
import os
import re

if __name__ == "__main__":
    xmlin = 'D:/BaiduYunDownload/CaltechPestrain2VOC/xml'
    xmlout = 'D:/BaiduYunDownload/CaltechPestrain2VOC/newxml'
    files = os.listdir(xmlin)
    #编译一个pattern
    pattern = re.compile('people')
    #每张图片进行判断
    for file in files:
        f = open(os.path.join(xmlin,file), 'r')
        content = f.read()
        f.close()
        result = re.search('people', content)
        if (result!=None):
            updateFile = pattern.sub('person', content)
        else:
            updateFile = content
        with open(os.path.join(xmlout,file), 'w') as fout:
            fout.write(updateFile)
        print ('updating file {}'.format(file))


