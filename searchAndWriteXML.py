#!/usr/bin/python3
# coding: utf-8

import os, sys
from PIL import Image, ImageDraw, ImageFont
import cv2
import tensorflow as tf
import xml.etree.ElementTree as ET
from pylab import *
import numpy as np

def getRegion_u(ptsList, size =320):  # size = 320
	# ptsList =[xmin, xmax, ymin, ymax]
	a = ptsList[0] // size
	b = ptsList[1] // size
	c = ptsList[2] // size
	d = ptsList[3] // size
	a = int(a)
	b = int(b)
	c = int(c)
	d = int(d)
	ijList = [(c, a), (c, b), (d, a), (d, b)]
	print("ijList before sort():",ijList)
	res = []
	for i in range(len(ijList)):
		if ijList[1] not in res:
			res.append(ijList[i])
	# res是去重之后的list
	# ijList_u = np.unique(ijList)
	ijList_u = res
	print("ijList:", ijList)
	print("ijList_u", res)
	boxList = []
	for ij in ijList_u:
		box = (size * ij[1], size * ij[0], size * (ij[1] + 1), size * (ij[0] + 1))
		boxList.append(box)
	return boxList

def drawbox(ptsList, draw_, str_text=None):
	p1 = ptsList[0]# xmin
	p2 = ptsList[1]# xmax
	p3 = ptsList[2]# ymin
	p4 = ptsList[3]# ymax
	box = [(p1, p3), (p2, p4)]
	draw_.rectangle(box, outline=(255, 255, 255))
	pts_list = ((p1, p3), (p1, p4), (p2, p4), (p2, p3), (p1, p3))
	draw_.line(pts_list, width=5, fill=(244, 25, 215))
	if str_text is not None:
		draw_.text((p1, p3), str_text, fill=(244, 25, 215))

def getBoxIJ(i_, j_,size):
	box = (size*j_, size*i_, size*(j_+1), size*(i_+1))
	return box

# img_path = "DJI ROCO/robomaster_Final Tournament/image"
# anno_path = "DJI ROCO/robomaster_Final Tournament/image_annotation"
img_path = "DJI ROCO/robomaster_North China Regional Competition/image"
anno_path = "DJI ROCO/robomaster_North China Regional Competition/image_annotation"
# test_img_path = "test/image"
# test_anno_path = "test/image_annotation"
out_img_path = "DJIDATACUT/image"
out_anno_path = "DJIDATACUT/image_annotation"
img_dirs = os.listdir(img_path)
anno_dirs = os.listdir(anno_path)
# test_img_dirs = os.listdir(test_img_path)
# test_anno_dirs = os.listdir(test_anno_path)




for file in img_dirs:
	print("file in test:", file)
	pil_img = Image.open(img_path + '/' + file)
	# pil_img_copy = pil_img.copy()
	# draw = ImageDraw.Draw(pil_img_copy)
	arr_pil_img = array(pil_img)
	origin_img_file_name = os.path.splitext(file)[0]
	tree = ET.parse(anno_path + '/' + os.path.splitext(file)[0] + '.xml')
	root_annotation = tree.getroot()
	filename = []
	size = []
	width = []
	height = []
	object_name_other = []
	bndbox_other = []
	object_name_armor = []
	bndbox_armor = []
	ijList_other = []
	ijList_armor = []
	size = 320
	flag_cross = [
		[0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0]
	]
	A_xmin = B_xmin = A_xmax = B_xmax =0
	A_ymin = B_ymin = A_ymax = B_ymax =0
	for i in range(3):
		for j in range(6):
			offset_xy = (320*j, 320*i)
			offset_x = 320*j
			offset_y = 320*i
			A_xmin = float(320*j)# 原始的ij方块坐标
			A_ymin = float(320*i)
			A_xmax = float(320*(j+1))
			A_ymax = float(320*(i+1))
			for object in root_annotation.iter('object'):
				# if object.find('name').text == 'armor':
				p1 = B_xmin = float(object.find('bndbox').find('xmin').text)# 原始的标签方块的坐标
				p3 = B_ymin = float(object.find('bndbox').find('ymin').text)
				p2 = B_xmax = float(object.find('bndbox').find('xmax').text)
				p4 = B_ymax = float(object.find('bndbox').find('ymax').text)
				ptsList = [p1, p2, p3, p4]
				xmin = max(A_xmin, B_xmin)
				ymin = max(A_ymin, B_ymin)
				xmax = min(A_xmax, B_xmax)
				ymax = min(A_ymax, B_ymax)
				# 判断是否有交集
				if(xmin > xmax or ymin > ymax):
					#flag_cross[i][j] = 0
					continue
				else:
					# 有
					flag_cross[i][j] = 1
					true_xmin = float("%.3f" % (xmin - offset_x))
					true_xmax = float("%.3f" % (xmax - offset_x))
					true_ymin = float("%.3f" % (ymin - offset_y))
					true_ymax = float("%.3f" % (ymax - offset_y))
					# true_xmin =  (xmin - offset_x)
					# true_xmax =  (xmax - offset_x)
					# true_ymin =  (ymin - offset_y)
					# true_ymax =  (ymax - offset_y)
					tuple_xy = (true_xmin, true_ymin, true_xmax, true_ymax)
					tuple_ij = (i, j)
					if object.find('name').text == 'armor':
						armor_name_str =   object.find('armor_color').text[0].upper() +object.find('armor_color').text[1:] \
						+ 'Armor' + object.find('armor_class').text[0].upper() +object.find('armor_class').text[1:]
						# print("armor_name :", armor_name_str)
						object_name_armor.append(armor_name_str)
						bndbox_armor.append(tuple_xy)
						ijList_armor.append(tuple_ij)
					else:
						other_name_str = object.find('name').text[0].upper() +object.find('name').text[1:]
						# print("other_name :", other_name_str)
						object_name_other.append(other_name_str)
						bndbox_other.append(tuple_xy)
						ijList_other.append(tuple_ij)
	# print("othertype: ",object_name_other)
	# print("bndbox: ", bndbox_other)
	# print("ijListother: ", ijList_other)
	# print("armortype: ", object_name_armor)
	# print("ijListarmor: ", ijList_armor)# 得到那些图片碎片是要保存的
	# print(flag_cross)
	for i in range(3):
		for j in range(6):
			# 再来一次便利 这次往碎片里写属性
			if flag_cross[i][j]:
				file_str = origin_img_file_name + '_' + str(i) + str(j)
				# 这个被保存的数据集碎片
				# 首先对图片进行保存和可视化处理
				file_str_img = file_str + '.jpg'
				box = getBoxIJ(i, j, 320)
				region_pil = pil_img.crop(box)
				# region_pil_copy = region_pil.copy()
				# draw = ImageDraw.Draw(region_pil_copy)
				# region_arr = array(region_pil)

				region_pil.save(out_img_path + '/' + file_str_img)
				# 可视化
				# for a in range(len(ijList_other)):
				# 	if(ijList_other[a] == (i,j)):
						# pass
						# draw.rectangle(bndbox_other[a], outline=(240, 223, 53))
						# draw.text((bndbox_other[a][0], bndbox_other[a][1]), object_name_other[a], fill=(240, 223, 53))
				# for a in range(len(ijList_armor)):
					# if(ijList_armor[a] == (i,j)):
						# pass
						# print("arawing: ij", i, j)
						# draw.rectangle(bndbox_armor[a], outline=(219, 144, 244))
						# draw.text((bndbox_armor[a][0], bndbox_armor[a][1]), object_name_armor[a], fill=(219, 144, 244))
				# figure()
				# region_copy_arr = array(region_pil_copy)
				# imshow(region_copy_arr)
				# title(file_str_img)

				# 写xml
				root_new = ET.Element('annotation')
				file_str_xml = file_str + '.xml'
				# object_inxml_other = []
				# object_inxml_armor = []
				file_name = ET.SubElement(root_new, 'filename')
				file_name.text = file_str_img
				for a in range(len(ijList_other)):
					if(ijList_other[a] == (i,j)):
						object = ET.SubElement(root_new, 'object')
						object_name = ET.SubElement(object, 'name')
						object_name.text = object_name_other[a]
						object_bndbox = ET.SubElement(object, 'bndbox')
						bnbox_x1 = ET.SubElement(object_bndbox, 'xmin')
						bnbox_x1.text = str(bndbox_other[a][0])
						bnbox_y1 = ET.SubElement(object_bndbox, 'ymin')
						bnbox_y1.text = str(bndbox_other[a][1])
						bnbox_x2 = ET.SubElement(object_bndbox, 'xmax')
						bnbox_x2.text = str(bndbox_other[a][2])
						bnbox_y2 = ET.SubElement(object_bndbox, 'ymax')
						bnbox_y2.text = str(bndbox_other[a][3])
						bndbox_width = ET.SubElement(object_bndbox, 'width')
						bndbox_width.text = ("%.3f" % (bndbox_other[a][2] - bndbox_other[a][0]))
						bndbox_height = ET.SubElement(object_bndbox, 'height')
						bndbox_height.text = ("%.3f" % (bndbox_other[a][3] - bndbox_other[a][1]))
				for a in range(len(ijList_armor)):
					if (ijList_armor[a] == (i, j)):
						object = ET.SubElement(root_new, 'object')
						object_name = ET.SubElement(object, 'name')
						object_name.text = object_name_armor[a]
						object_bndbox = ET.SubElement(object, 'bndbox')
						bnbox_x1 = ET.SubElement(object_bndbox, 'xmin')
						bnbox_x1.text = str(bndbox_armor[a][0])
						bnbox_y1 = ET.SubElement(object_bndbox, 'ymin')
						bnbox_y1.text = str(bndbox_armor[a][1])
						bnbox_x2 = ET.SubElement(object_bndbox, 'xmax')
						bnbox_x2.text = str(bndbox_armor[a][2])
						bnbox_y2 = ET.SubElement(object_bndbox, 'ymax')
						bnbox_y2.text = str(bndbox_armor[a][3])
						bndbox_width = ET.SubElement(object_bndbox, 'width')
						bndbox_width.text = ("%.3f" % (bndbox_armor[a][2] - bndbox_armor[a][0]))
						bndbox_height = ET.SubElement(object_bndbox, 'height')
						bndbox_height.text = ("%.3f" % (bndbox_armor[a][3] - bndbox_armor[a][1]))
				new_tree = ET.ElementTree(root_new)
				new_tree.write(out_anno_path + '/' + file_str_xml, encoding='utf-8')

			# else:
			# 	continue
# show()


