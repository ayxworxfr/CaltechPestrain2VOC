import shutil
import re, os, sys
from xml.dom.minidom import parse

class Filter:
    saveRoot = ''
    xmlPath = ''
    imagePath = ''
    xmlSavePath = ''
    imageSavePath = ''
    saveCount = 0
    saveStep = 5            # 保存步长，每saveStep张图片保存一张

    # root为xml和图片根目录, saveRoot为VOC2007保存目录
    def __init__(self, root, saveRoot):
        self.saveRoot = saveRoot
        self.xmlPath = root + '/xml'
        self.imagePath = root + '/image'
        self.xmlSavePath = saveRoot + '/Annotations'
        self.imageSavePath = saveRoot + '/JPEGImages'

    # 开始筛选
    def run(self):
        # delete the image folder path if it exists
        if not self.saveRoot.endswith('VOC2007'):
            print('保存路径有问题需要以VOC2007结尾！！！')
            return False
        if os.path.exists(self.saveRoot):
            shutil.rmtree(self.saveRoot)
        # create the image folder path
        if not os.path.exists(self.saveRoot):
            os.makedirs(self.xmlSavePath)
            os.makedirs(self.imageSavePath)
            os.makedirs(self.saveRoot + '/ImageSets/Main')

        print('开始筛选...')
        files = os.listdir(self.imagePath)
        total = files.__len__()
        count = 0
        for image_name in files:
            self.view(count, total)
            count += 1
            # 每saveStep张图片保存一张
            self.saveCount += 1
            if self.saveCount % self.saveStep != 0:
                continue

            flag = False        # 是否需要保存
            if(image_name.endswith('.jpg')):
                flag = self.parseFile(open(self.imagePath + '/' + image_name))
            if(flag):
                self.saveFile(image_name[0:-4])
        print('筛选结束')
    # 判断该文件是否需要保存
    def parseFile(self, file):
        return True

    def view(self, count, total):
        # 进度条步长
        step = 1
        # 进度条
        if count % step == 0:
            if count + 1 == total:
                percent = 100.0
                print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', count + 1, total), end='\n')
            else:
                percent = round(1.0 * count / total * 100, 2)
                print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', count + 1, total), end='\r')

    # 通过文件名称复制对应的xml文件和图片
    def saveFile(self, name):
        old_xml = self.xmlPath + '/' + name + '.xml'
        old_image = self.imagePath + '/' + name + '.jpg'
        new_xml = self.xmlSavePath + '/' + name + '.xml'
        new_image = self.imageSavePath + '/' + name + '.jpg'
        # 判断image是否存在
        if(os.path.isfile(old_image)):
            shutil.copyfile(old_image, new_image)
        # xml存在则直接保存，否则修改模板后保存
        if (os.path.isfile(old_xml)):
            shutil.copyfile(old_xml, new_xml)
        else:
            old_xml = os.getcwd() + '/data/mode.xml'
            self.updateXML(old_xml, name + '.jpg')
            shutil.copyfile(old_xml, new_xml)

    def updateXML(self, path, data):
        domTree = parse(path)
        # 文档根元素
        rootNode = domTree.documentElement

        filename = rootNode.getElementsByTagName("filename")[0]
        filename.childNodes[0].data = data

        with open(path, 'w') as f:
            # 缩进 - 换行 - 编码
            domTree.writexml(f, addindent='  ', encoding='utf-8')

if __name__ == '__main__':
    root = os.getcwd() + '/data'
    saveRoot = os.getcwd() + '/VOC2007'
    filter = Filter(root, saveRoot)
    filter.run()