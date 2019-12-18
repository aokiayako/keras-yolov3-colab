import os
import sys
import xml.etree.ElementTree as ET
from os import getcwd

year, image_set = ('2007', 'train_data')
# sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["paper", "cup"]

if len(sys.argv) > 1:
    classes = sys.argv[1:]

with open('model_data/voc_classes.txt', 'w') as f:
    f.write('\n'.join(classes))


def convert_annotation(year, image_id, list_file):
    in_file = open('VOCDevkit/VOC%s/Annotations/%s.xml' % (year, image_id.replace('.jpg', '')))
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)),
             int(float(xmlbox.find('ymin').text)),
             int(float(xmlbox.find('xmax').text)),
             int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()
list_file = open('model_data/model_%s.txt' % (image_set), 'w')

# 画像のリストを取得
img_list = os.listdir('%s/VOCDevkit/VOC%s/JPEGImages' % (wd, year))

# xmlの拡張子なしリストを取得
xml_list = []
for file in os.listdir('%s/VOCDevkit/VOC%s/Annotations' % (wd, year)):
    base_name, ext = os.path.splitext(file)
    if ext == '.xml':
        xml_list.append(base_name)

# 画像に対してアノテーションデータがあれば(=対応するxmlファイルがあれば)xmlからアノテーションデータを取得する
for image_id in img_list:
    if image_id[:-4] not in xml_list:
        continue
    image_file_path = '%s/VOCDevkit/VOC%s/JPEGImages/%s' % (wd, year, image_id)
    list_file.write(image_file_path)
    convert_annotation(year, image_id, list_file)
    list_file.write('\n')
list_file.close()
