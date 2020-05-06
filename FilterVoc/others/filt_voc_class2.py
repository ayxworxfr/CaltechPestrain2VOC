import shutil
import re, os, sys
from xml.dom.minidom import parse

class Filter:
    VOC_NAME = 'VOC2007'
    saveRoot = ''
    xmlPath = ''
    imagePath = ''
    xmlSavePath = ''
    imageSavePath = ''
    saveCount = 0
    # saveStep = 5            # 保存步长，每saveStep张图片保存一张
    save_classes = ['person']

    # root为xml和图片根目录, saveRoot为VOC2007保存目录
    def __init__(self, root, saveRoot):
        self.saveRoot = saveRoot
        self.xmlPath = root + '/' +  self.VOC_NAME + '/Annotations'
        self.imagePath =  root + '/' +  self.VOC_NAME + '/JPEGImages'
        self.xmlSavePath = saveRoot + '/Annotations'
        self.imageSavePath = saveRoot + '/JPEGImages'

    # 开始筛选
    def run(self):
        # delete the image folder path if it exists
        if not self.saveRoot.endswith(self.VOC_NAME):
            print('保存路径有问题需要以' + self.VOC_NAME + '结尾！！！')
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
            # if self.saveCount % self.saveStep != 0:
            #     continue

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
        else:
            pass
        # xml存在则筛选类别后保存
        if (os.path.isfile(old_xml)):
            self.filtAndSaveXML(old_xml, new_xml)
        else:
            pass

    def filtAndSaveXML(self, old_xml, new_xml):
        domTree = parse(old_xml)
        # 文档根元素
        rootNode = domTree.documentElement

        objects = rootNode.getElementsByTagName("object")

        i = 0
        length = objects.length
        while i < length:
            # 获取object类别名称
            name = objects[i].getElementsByTagName('name')[0].childNodes[0].data
            # 如果name在save_classes里则pass, 否则直接删除
            if(self.save_classes.__contains__(name)):
                pass
            else:
                objects[i].delete()
                # objects[i].childNodes.data = "test"
                # objects.pop(i)
                # length -= 1
                # continue
            i += 1


        with open(new_xml, 'w') as f:
            # 缩进 - 换行 - 编码
            domTree.writexml(f, addindent='  ', encoding='utf-8')

if __name__ == '__main__':
    root = os.getcwd() + '/data'
    saveRoot = os.getcwd() + '/VOC2007'
    filter = Filter(root, saveRoot)
    filter.run()