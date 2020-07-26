#!/usr/bin/python3
# coding: utf-8

import os, sys
from PIL import Image, ImageDraw, ImageFont
import cv2
import tensorflow as tf
import xml.etree.ElementTree as ET
from pylab import *
import numpy as np
import json

img_path0 = "DJI ROCO/robomaster_Final Tournament/image"
img_path1 = "DJI ROCO/robomaster_North China Regional Competition/image"
img_path2 = "DJI ROCO/robomaster_South China Regional Competition/image"
img_path3 = "DJI ROCO/robomaster_Central China Regional Competition/image"
anno_path0 = "DJI ROCO/robomaster_Final Tournament/image_annotation"
anno_path1 = "DJI ROCO/robomaster_North China Regional Competition/image_annotation"
anno_path2 = "DJI ROCO/robomaster_South China Regional Competition/image_annotation"
anno_path3 = "DJI ROCO/robomaster_Central China Regional Competition/image_annotation"

img_dirs0 = os.listdir(img_path0)
img_dirs1 = os.listdir(img_path1)
img_dirs2 = os.listdir(img_path2)
img_dirs3 = os.listdir(img_path3)
anno_dirs0 = os.listdir(anno_path0)
anno_dirs1 = os.listdir(anno_path1)
anno_dirs2 = os.listdir(anno_path2)
anno_dirs3 = os.listdir(anno_path3)

img_dirs = [img_dirs0, img_dirs1, img_dirs2, img_dirs3]
img_path = [img_path0, img_path1, img_path2, img_path3]
anno_dirs = [anno_dirs0, anno_dirs1, anno_dirs2, anno_dirs3]
anno_path = [anno_path0, anno_path1, anno_path2, anno_path3]

test_img_path = "DJI ROCO/test/image"
test_anno_path = "DJI ROCO/test/image_annotation"
# out_img_path = "DJIDATACUT/test_imag"
# img_dirs = os.listdir(img_path)
test_img_dirs = [os.listdir(test_img_path)]
test_anno_dirs = [os.listdir(test_anno_path)]

dict_category_id = {}
categoties = []
categoties_split_others_armors = []
str_others = []
str_armors = []
for i in range(1):
	for file in test_anno_dirs[i]:
		pass

