import os, shutil
import xml.etree.cElementTree as ET

root = os.getcwd()
path_xml = [root + '/data/VOC2007/Annotations']
path_image = [root + '/data/VOC2007/JPEGImages']
out_image = root + '/out/JPEGImages'
out_xml = root + '/out/Annotations'
if not os.path.exists(out_xml):
    os.makedirs(out_xml)
if not os.path.exists(out_image):
    os.makedirs(out_image)

# CLASSES = [
#            "bottle",
#            "dog", "motorbike", "person",
#            "pottedplant","sofa"]
CLASSES = ["person"]
for xml_path in path_xml:
    xml_list = os.listdir(xml_path)
print('开始筛选...')
for item in xml_list:
    flag = False
    path_xml = os.path.join(xml_path, item)
    tree = ET.parse(path_xml)
    root = tree.getroot()

    for child in root.findall('object'):
        name = child.find('name').text
        if not name in CLASSES:
            root.remove(child)
        else:
            flag = True
    # 包含需要的类别才保存
    if flag:
        image_name = item[0:-4] + '.jpg'

        for image_path in path_image:
            old_image = image_path + '/' + image_name
            # 没有找到文件继续循环，否则跳出循环
            if not os.path.exists(old_image):
                continue
            break

        new_image = out_image + '/' + image_name
        # 复制图片
        shutil.copyfile(old_image, new_image)
        tree.write(os.path.join(out_xml, item))
print('筛选完成！！！')