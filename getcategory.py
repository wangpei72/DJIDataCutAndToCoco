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

json_dict = {}
dict_category_id = {}
categoties = []
categoties_split_others_armors = []
str_others = []
str_armors = []
for i in range(4):
	for file in anno_dirs[i]:
		tree = ET.parse(anno_path[i] + '/' + file)
		root_annotation = tree.getroot()
		for object in root_annotation.iter('object'):
			name_txt = object.find('name').text
			if name_txt != 'armor':
				other_name_str = object.find('name').text[0].upper() + object.find('name').text[1:]
				if other_name_str not in str_others:
					str_others.append(other_name_str)
					categoties.append(other_name_str)
				else:
					continue
			else:
				armor_class = object.find('armor_class').text
				armor_color = object.find('armor_color').text
				armor_name_str = object.find('armor_color').text[0].upper() + object.find('armor_color').text[1:] + 'Armor' + object.find('armor_class').text[0].upper() + object.find('armor_class').text[1:]
				armor_txt = armor_name_str
				if armor_txt not in str_armors:
					str_armors.append(armor_txt)
					categoties.append(armor_txt)
				else:
					continue
# categoties_split_others_armors.append(str_others)
# categoties_split_others_armors.append(str_armors)
dict_category_id = dict.fromkeys(categoties, 0)
for i in range(len(categoties)):
	dict_category_id[categoties[i]] = i+1
print(dict_category_id)
print(categoties)
print("total :", len(categoties))
print("others :", len(str_others))
print("armors :", len(str_armors))

file = open("categories_All.txt", "w+")
file.write("category_dict: \n" + str(dict_category_id))
file.write("\ncategory: \n" + str(categoties))
file.write("\ntotal: " + str(len(categoties)))
file.write("\nothers: " + str(len(str_others)))
file.write("\narmors: " + str(len(str_armors)))
file.close()

categoryList = []
# itemToAdd = {}
for i in range(len(categoties)):
	itemToAdd = {}
	itemToAdd["name"] = categoties[i]
	itemToAdd["id"] = dict_category_id[categoties[i]]
	if('Armor' in categoties[i]):
		itemToAdd["supercategory"] = 'Armor'
	else:
		itemToAdd["supercategory"] = categoties[i]
	categoryList.append(itemToAdd)
json_dict["categories"] = categoryList

with open("category.json", "w+", encoding='utf-8') as f:
	json.dump(json_dict, f, indent=2, sort_keys=True, separators=(',', ': '))




