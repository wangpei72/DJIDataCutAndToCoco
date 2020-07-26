#!/usr/bin/python3
# coding: utf-8

import os, sys
import json
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from pylab import *

def getBoxIJ(i_, j_,size):
	box = (size*j_, size*i_, size*(j_+1), size*(i_+1))
	return box

img_path0 = "DJI ROCO/robomaster_Final Tournament/image"
img_path1 = "DJI ROCO/robomaster_North China Regional Competition/image"
img_path2 = "DJI ROCO/robomaster_South China Regional Competition/image"
img_path3 = "DJI ROCO/robomaster_Central China Regional Competition/image"
anno_path0 = "DJI ROCO/robomaster_Final Tournament/image_annotation"
anno_path1 = "DJI ROCO/robomaster_North China Regional Competition/image_annotation"
anno_path2 = "DJI ROCO/robomaster_South China Regional Competition/image_annotation"
anno_path3 = "DJI ROCO/robomaster_Central China Regional Competition/image_annotation"

test_img_path = ["DJI ROCO/test/image"]
test_anno_path = ["DJI ROCO/test/image_annotation"]

test_img_dirs = os.listdir(test_img_path[0])
test_anno_dirs = os.listdir(test_anno_path[0])
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
out_img_path = "DJIDATACUT/newcut/image"
out_anno_path = "DJIDATACUT/newcut/image_annotation/"

with open("category.json", encoding='utf-8') as f:
	json_dict = json.load(f)
# 此时json_dict中已经有了categories的键值对
# print(json_dict["categories"])

categories_dict = {'BlueArmor5': 9, 'GreyArmorNone': 16, 'RedArmorNone': 11, 'Car': 1, 'GreyArmor8': 30, 'RedArmor4': 27, 'BlueArmor3': 26, 'GreyArmor2': 23, 'BlueArmor8': 20, 'GreyArmor5': 14, 'BlueArmorNone': 24, 'RedArmor7': 29, 'BlueArmor1': 17, 'Ignore': 25, 'RedArmor8': 12, 'Watcher': 7, 'RedArmor3': 4, 'GreyArmor4': 15, 'GreyArmor3': 22, 'BlueArmor7': 8, 'BlueArmor4': 2, 'RedArmor6': 13, 'BlueArmor2': 10, 'RedArmor5': 6, 'RedArmor1': 3, 'RedArmor2': 5, 'GreyArmor7': 19, 'GreyArmor6': 31, 'GreyArmor1': 28, 'Base': 18, 'BlueArmor6': 21}
img_dict = {}
img_dict_fromid = {}

imagesList = []
annotationsList = []
annotationsList_val = []
annotationsList_test = []

img_file_name = []
object_name_other = []
bndbox_other = []
object_name_armor = []
bndbox_armor = []
ijList_other = []
ijList_armor = []
id_list_armor = []
# img_id_list_armor = []
category_id_list_armor = []
img_file_list_armor = []

id_list_other = []
# img_id_list_other = []
category_id_list_other = []
img_file_list_other = []

id_list_img = []
image_id = 0

object_id = 0
# 获取碎片记录地图以及各属性值
for index in range(1):
	for file in test_img_dirs:
	# for file in img_dirs[index]:
		print("批序号： file in test:", index, file)
		if (file[0] == '.'):
			file = file[2:]
		# pil_img = Image.open(img_path[index] + '/' + file)
		pil_img = Image.open(test_img_path[0] + '/' + file)
		arr_pil_img = array(pil_img)
		origin_img_file_name = os.path.splitext(file)[0]
		# tree = ET.parse(anno_path[index] + '/' + os.path.splitext(file)[0] + '.xml')
		tree = ET.parse(test_anno_path[0] + '/' + os.path.splitext(file)[0] + '.xml')
		root_annotation = tree.getroot()
		# tuple_ij = (i, j)
		for object in root_annotation.iter('object'):
			if object.find('name').text == 'car':
				p1 = B_xmin = float(object.find('bndbox').find('xmin').text)  # 原始的标签方块的坐标
				p3 = B_ymin = float(object.find('bndbox').find('ymin').text)
				p2 = B_xmax = float(object.find('bndbox').find('xmax').text)
				p4 = B_ymax = float(object.find('bndbox').find('ymax').text)
				ptsList = [p1, p2, p3, p4]
				width = B_xmax - B_xmin
				height = B_ymax - B_ymin
				true_width = 1.2 * width
				true_height = 1.2 * height
				true_xmin = float("%.3f" % (0.1 * width))
				true_xmax = float("%.3f" % (1.1 * width))
				true_ymin = float("%.3f" % (0.1 * height))
				true_ymax = float("%.3f" % (1.1 * height))
				tuple_xy = (true_xmin, true_ymin, true_xmax, true_ymax)
				box_x1 = B_xmin - 0.1 * width
				box_x2 = B_xmax + 0.1 * width
				box_y1 = B_ymin - 0.1 * height
				box_y2 = B_ymax + 0.1 * height
				box = (box_x1, box_y1, box_x2, box_y2)
				object_id += 1
				image_id += 1
				# 存数据
				id_list_img.append(image_id)
				file_str = origin_img_file_name + '_' + str(image_id)
				file_str_img = file_str + '.jpg'
				img_file_name.append(file_str_img)
				img_dict[file_str_img] = image_id
				img_dict_fromid[str(image_id)] = file_str_img
				region_pil = pil_img.crop(box)
				region_pil.save(out_img_path + '/' + file_str_img)

				other_name_str = object.find('name').text[0].upper() + object.find('name').text[1:]
				cate_id = categories_dict[other_name_str]
				object_name_other.append(other_name_str)
				bndbox_other.append(tuple_xy)
				id_list_other.append(object_id)
				category_id_list_other.append(cate_id)
				img_file_list_other.append(file_str_img)
				# 保存图

				for object in root_annotation.iter("object"):
					if object.find('name').text == 'armor':
						p1_a = A_xmin = float(object.find('bndbox').find('xmin').text)  # 原始的标签方块的坐标
						p3_a = A_ymin = float(object.find('bndbox').find('ymin').text)
						p2_a = A_xmax = float(object.find('bndbox').find('xmax').text)
						p4_a = A_ymax = float(object.find('bndbox').find('ymax').text)
						xmin = max(A_xmin, B_xmin)
						ymin = max(A_ymin, B_ymin)
						xmax = min(A_xmax, B_xmax)
						ymax = min(A_ymax, B_ymax)
						if (xmin > xmax or ymin > ymax):
							continue
						else:
							if(A_xmin<B_xmin):
								print("bndbox out of range,repairing...")
								A_xmin = B_xmin
							if(A_ymin<B_ymin):
								print("bndbox out of range,repairing...")
								A_ymin = B_ymin
							if(A_xmax > B_xmax):
								print("bndbox out of range,repairing...")
								A_xmax = B_xmax
							if(A_ymax > B_ymax):
								print("bndbox out of range,repairing...")
								A_ymax = B_ymax
							width = A_xmax - A_xmin
							height = A_ymax - A_ymin
							true_width = 1.2 * width
							true_height = 1.2 * height
							true_xmin = float("%.3f" % (0.1 * width))
							true_xmax = float("%.3f" % (1.1 * width))
							true_ymin = float("%.3f" % (0.1 * height))
							true_ymax = float("%.3f" % (1.1 * height))
							tuple_xy_a = (true_xmin, true_ymin, true_xmax, true_ymax)
							armor_name_str = object.find('armor_color').text[0].upper() + object.find('armor_color').text[1:] + 'Armor' + \
											 object.find('armor_class').text[0].upper() + object.find('armor_class').text[1:]
							object_id += 1
							cate_id = categories_dict[armor_name_str]
							object_name_armor.append(armor_name_str)
							bndbox_armor.append(tuple_xy_a)
							id_list_armor.append(object_id)
							category_id_list_armor.append(cate_id)
							img_file_list_armor.append(file_str_img)
				# 写xml
for a in range(len(id_list_img)):
	root_new = ET.Element('annotation')
	file_str_xml = os.path.splitext(img_dict_fromid[str(a+1)])[0] + '.xml'
	object_inxml_other = []
	object_inxml_armor = []
	file_name = ET.SubElement(root_new, 'filename')
	file_name.text = img_dict_fromid[str(a+1)]
	size = ET.SubElement(root_new, 'size')
	width = ET.SubElement(size, 'width')
	width.text = str(320)
	height = ET.SubElement(size, 'height')
	height.text = str(320)
	# for a in range(len(ijList_other)):
	# 	if (ijList_other[a] == (i, j)):
	# 		pass
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
			pass
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




			# box = getBoxIJ(i, j, 320)

			# region_pil_copy = region_pil.copy()
			# draw = ImageDraw.Draw(region_pil_copy)
			# region_arr = array(region_pil)

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

for i in range(len(id_list_img)):
	itemToAdd = {}
	itemToAdd["file_name"] = img_file_name[i]
	itemToAdd["height"] = 320
	itemToAdd["width"] = 320
	itemToAdd["id"] = id_list_img[i]
	imagesList.append(itemToAdd)
# print(imagesList)
json_dict["images"] = imagesList

json_dict_train = json_dict

json_dict_val = {}
json_dict_test = {}
json_dict_val["images"] = imagesList
json_dict_test["images"] = imagesList
json_dict_val["categories"] = json_dict["categories"]
json_dict_test["categories"] = json_dict["categories"]

for i in range(len(id_list_armor)):
	# print(i)
	x1 = bndbox_armor[i][0]
	y1 = bndbox_armor[i][1]
	x2 = bndbox_armor[i][2]
	y2 = bndbox_armor[i][3]
	w = x2 - x1
	h = y2 - y1
	w = float("%.0f" % w)
	h = float("%.0f" % h)
	itemToAdd = {}
	itemToAdd["iscrowd"] = 0
	itemToAdd["area"] = float("%.0f" % (w*h))
	itemToAdd["image_id"] = img_dict[img_file_list_armor[i]]
	itemToAdd["bbox"] = [x1, y1, w, h]
	itemToAdd["category_id"] = category_id_list_armor[i]
	id = itemToAdd["id"] = id_list_armor[i]
	itemToAdd["segmentation"] = [[x1, y1, x2, y2]]
	if ((id % 10) in [1, 2, 3, 4, 5, 6, 0]):
		# print("<7", id%10)
		# print(id)
		annotationsList.append(itemToAdd)
	elif ((id % 10) in [7, 8]):
		# print("7<9", id%10)
		annotationsList_test.append(itemToAdd)
	elif((id % 10) == 9):
		# print("9", id%10)
		annotationsList_val.append(itemToAdd)

for i in range(len(id_list_other)):
	x1 = bndbox_other[i][0]
	y1 = bndbox_other[i][1]
	x2 = bndbox_other[i][2]
	y2 = bndbox_other[i][3]
	w = x2 - x1
	h = y2 - y1
	w = float("%.0f" % w)
	h = float("%.0f" % h)
	itemToAdd = {}
	itemToAdd["iscrowd"] = 0
	itemToAdd["area"] = float("%.0f" % (w*h))
	itemToAdd["image_id"] = img_dict[img_file_list_other[i]]
	itemToAdd["bbox"] = [x1, y1, w, h]
	itemToAdd["category_id"] = category_id_list_other[i]
	d = itemToAdd["id"] = id_list_other[i]
	itemToAdd["segmentation"] = [[x1, y1, x2, y2]]
	if ((id % 10) in [1, 2, 3, 4, 5, 6, 0]):
		# print(id)
		annotationsList.append(itemToAdd)
	elif ((id % 10) in [7, 8]):
		annotationsList_test.append(itemToAdd)
	elif((id % 10) == 9):
		annotationsList_val.append(itemToAdd)
print("train", len(annotationsList))
print("test", len(annotationsList_test))
print("val", len(annotationsList_val))

json_dict_train["annotations"] = annotationsList
json_dict_val["annotations"] = annotationsList_val
json_dict_test["annotations"] = annotationsList_test

with open(out_anno_path+"new_test.json", "w+", encoding='utf-8') as f1:
	json.dump(json_dict_test, f1, indent=2, sort_keys=False, ensure_ascii=False)

with open(out_anno_path+"new_train.json", "w", encoding='utf-8') as f2:
	json.dump(json_dict_train, f2, indent=2, sort_keys=False, ensure_ascii=False)

with open(out_anno_path+"new_val.json", "w+", encoding='utf-8') as f3:
	json.dump(json_dict_val, f3, indent=2, sort_keys=False, ensure_ascii=False)
