#!/usr/bin/python3
# coding: utf-8

import os, sys
from PIL import Image, ImageDraw, ImageFont
import cv2
import tensorflow as tf
import xml.etree.ElementTree as ET
from pylab import *
import numpy as np


test_img_path = "DJI ROCO/test/image"
test_anno_path = "DJI ROCO/test/image_annotation"
test_img_dirs = os.listdir(test_img_path)
# 标签文件夹中所有文件列表
test_anno_dirs = os.listdir(test_anno_path)

# for file in test_img_dirs:
# 	tree = ET.parse(test_anno_path + file)
# 	tree = ET.parse(anno_path + "/" + "VW_CH3ENTERPRIZEVsTaurus_BO2_1_4.xml")
	# root = tree.getroot()

root = ET.Element('annotation')
object = ET.SubElement(root, 'object')
name = ET.SubElement(object, 'name')
name.text = 'car'
bndbox = ET.SubElement(object, 'bndbox')
bndbox.text = 'test'
object2 = ET.SubElement(root, 'object')
name2 = ET.SubElement(object2, 'name')
name2.text = 'armor'
ET.dump(root)
tree = ET.ElementTree(root)
tree.write('test.xml', encoding='utf-8')
xml_str = ET.tostring(root)



