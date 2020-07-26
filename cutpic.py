#!/usr/bin/python3
# coding: utf-8

import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import tensorflow as tf
import xml.etree.ElementTree as ET
from pylab import *
import numpy as np


def getRegion_ij(ptsList, size):  # size = 320
	# ptsList =[xmin, xmax, ymin, ymax]
	a = ptsList[0] // size
	b = ptsList[1] // size
	c = ptsList[2] // size
	d = ptsList[3] // size
	a = int(a)
	b = int(b)
	c = int(c)
	d = int(d)
	ijList = [[c, a], [c, b], [d, a], [d, b]]
	return ijList

def getRegion_ij_u(ptsList, size):  # size = 320
	# ptsList =[xmin, xmax, ymin, ymax]
	a = ptsList[0] // size
	b = ptsList[1] // size
	c = ptsList[2] // size
	d = ptsList[3] // size
	a = int(a)
	b = int(b)
	c = int(c)
	d = int(d)
	ijList = [[c, a], [c, b], [d, a], [d, b]]
	res = []
	for i in range(len(ijList)):
		if ijList[1] not in res:
			res.append(ijList[i])
	# res是去重之后的list
	# ijList_u = np.unique(ijList)
	ijList_u = res
	return ijList_u


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
	# box1 = (size*a, size*c, size*(a+1), size*(c+1))
	# box2 = (size*b, size*c, size*(b+1), size*(c+1))
	# box3 = (size*a, size*d, size*(a+1), size*(d+1))
	# box4 = (size*b, size*d, size*(b+1), size*(d+1))
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
		# textsize =15
		# ft = ImageFont.truetype("~/PycharmProjects/untitled/arialuni.ttf", textsize)
		draw_.text((p1, p3), str_text, fill=(244, 25, 215))


def showBoxInSrc(pil_img_):
	img_for_show = array(pil_img_)
	figure()
	imshow(img_for_show)
	title('box_in_origin_picture')
	# x = [p1, p1, p2, p2]
	# y = [p3, p3, p4, p4]
	# plot(x[:2], y[1:3], 'w')  # 画线框出车子
	# plot(x[1:3], y[2:], 'w')
	# plot(x[2:], y[1:3], 'w')
	# plot(x[1:3], y[:2], 'w')

# 获取当前的多物体（车子或者装甲板的）新属性 分割之后图片中的xywh(json格式)的属性
# 需要求出的是新的四个点 计算出宽和高
# 思路 分类讨论被切割情况不同 三种情况来计算
# 没有去重的按照左上 右上 左下 右下 顺序计算出四个ij
def getBoxSegmentXYForObject(ijList, ijList_u, ptsList, size=320):
	shorter = len(ijList) - len(ijList_u)
	# ptsList =[xmin, xmax, ymin, ymax]
	xmin = ptsList[0]
	xmax = ptsList[1]
	ymin = ptsList[2]
	ymax = ptsList[3]
	print("xmin %f ymin %f xmax %f ymax %f" %(xmin, ymin, xmax, ymax))
	ObjectSegmentListWithXYWH = []
	newXY_x1 = newXY_x2 = newXY_y1 = newXY_y2 = 0
	if(shorter == 0):
		print("种类：被切割4块",end=" ")
		for x in range(4):
			i = ijList[x - 1][0]
			j = ijList[x - 1][1]
			if(x == 0):
				newXY_x1 = xmin - size*j
				newXY_y1 = ymin - size*i
				newXY_x2 = size*(j+1) - size*j
				newXY_y2 = size*(i+1) - size*i
			elif(x == 1):
				newXY_x1 = size*j - size*j
				newXY_y1 = ymin - size*i
				newXY_x2 = xmax - size*j
				newXY_y2 = size*(i+1) - size*i
			elif(x == 2):
				newXY_x1 = xmin - size*j
				newXY_y1 = size*i
				newXY_x2 = size*(j+1) - size*j
				newXY_y2 = ymax - size*i
			else:
				newXY_x1 = size*j - size*j
				newXY_y1 = size*i - size*i
				newXY_x2 = xmax - size*j
				newXY_y2 = ymax - size*i
			width = newXY_x2 - newXY_x1
			height = newXY_y2 - newXY_y1
			ObjectSegmentListWithXYWH.append((newXY_x1, newXY_y1, width, height))
	elif(shorter == 2):
		print("被切割块数 2", end=" ")
		if(ijList[0] == ijList[1]):
			print("竖切：")
			for x in range(2):
				i = ijList_u[x][0]
				j = ijList_u[x][1]
				print("竖切ij = ", i, j, end='')
				if(x == 0):
					newXY_x1 = xmin - size*j
					newXY_y1 = ymin - size*i
					newXY_x2 = xmax - size*j
					newXY_y2 = size*(i+1) - size*i
				else:
					newXY_x1 = xmin - size*j
					newXY_y1 = size*i - size*i
					newXY_x2 = xmax - size*j
					newXY_y2 = ymax - size*i
				width = newXY_x2 - newXY_x1
				height = newXY_y2 - newXY_y1
				ObjectSegmentListWithXYWH.append((newXY_x1, newXY_y1, width, height))
		else:
			print("横切:")
			for x in range(2):
				i = ijList_u[x][0]
				j = ijList_u[x][1]
				print("横切ij = ", i, j, end='')
				if(x == 0):
					newXY_x1 = xmin - size*j
					newXY_y1 = ymin - size*i
					newXY_x2 = size*(j+1) - size*j
					newXY_y2 = ymax - size*i
				else:
					newXY_x1 = size*j - size*j
					newXY_y1 = ymin - size*i
					newXY_x2 = xmax - size*j
					newXY_y2 = ymax - size*i
				width = newXY_x2 - newXY_x1
				height = newXY_y2 - newXY_y1
				# print("横切各值x1 x2 y1 y2 ",newXY_x1,newXY_y1,newXY_x2,newXY_y2)
				ObjectSegmentListWithXYWH.append((newXY_x1, newXY_y1, width, height))
	elif(shorter == 3):
		print("种类 被切割块数 1：", end=" ")
		i = ijList_u[0][0]
		j = ijList_u[0][1]
		newXY_x1 = xmin - size*j
		newXY_y1 = ymin - size*i
		newXY_x2 = xmax - size*j
		newXY_y2 = ymax - size*i
		width = newXY_x2 - newXY_x1
		height = newXY_y2 - newXY_y1
		ObjectSegmentListWithXYWH.append((newXY_x1, newXY_y1, width, height))
	# print("被切割块数：", len(ObjectSegmentListWithXYWH))
	# for i in range(len(ObjectSegmentListWithXYWH)):
	# 	print("第 %d 个块的xywh :"%(i+1),ObjectSegmentListWithXYWH[i])


	return ObjectSegmentListWithXYWH



img_path = "DJI ROCO/robomaster_Final Tournament/image"
anno_path = "DJI ROCO/robomaster_Final Tournament/image_annotation"
test_img_path = "DJI ROCO/test/image"
test_anno_path = "DJI ROCO/test/image_annotation"
out_img_path = "DJIDATACUT/test_imag"
img_dirs = os.listdir(img_path)
anno_dirs = os.listdir(anno_path)

# 图片文件夹中所有文件路径列表
test_img_dirs = os.listdir(test_img_path)
# 标签文件夹中所有文件列表
test_anno_dirs = os.listdir(test_anno_path)
print("test_img_dirs :", test_img_dirs)
# a = 176//320
# print("a**********: ", a)
for file in test_img_dirs:
	print("file in test_img_dirs", file)
	# 获取当前路径下的文件，生成pilimg的实体
	pil_img = Image.open(test_img_path + '/' + file)
	# pil_img = Image.open(img_path+"/"+"VW_CH3ENTERPRIZEVsTaurus_BO2_1_4.jpg")
	pil_img_copy = pil_img.copy()
	draw = ImageDraw.Draw(pil_img_copy)
	img = array(pil_img)
	# figure()
	# imshow(img)
	# title(file)
	# print(img_path+"/"+"VW_CH3ENTERPRIZEVsTaurus_BO2_1_4.jpg")
	# for file in dirs:
	tree = ET.parse(test_anno_path + '/' + os.path.splitext(file)[0] + '.xml')
	# tree = ET.parse(anno_path + "/" + "VW_CH3ENTERPRIZEVsTaurus_BO2_1_4.xml")
	root = tree.getroot()
	boxs1 = root.findall("object",)
	for object in root.iter("object"):
		if object.find('name').text == 'armor':
			car = object.find('bndbox')
			p1 = car_xmin = float(car.find('xmin').text)
			p3 = car_ymin = float(car.find('ymin').text)
			p2 = car_xmax = float(car.find('xmax').text)
			p4 = car_ymax = float(car.find('ymax').text)
			ptsList = [p1, p2, p3, p4]
			drawbox(ptsList, draw, 'car')# 画在了copy上
			boxs = getRegion_u(ptsList, 320)
			ijList_u = getRegion_ij_u(ptsList, 320)
			ijList = getRegion_ij(ptsList, 320)
			car_segment = getBoxSegmentXYForObject(ijList, ijList_u, ptsList, 320)
			# print("test ij :", ijList[0][0], ijList[0][1])
			for i in range(len(boxs)):
				region_pil = pil_img.crop(boxs[i])
				region_arr = array(region_pil)
				figure()
				imshow(region_arr)
				out_img_file = os.path.splitext(file)[0] + "_" + str(ijList_u[i][0]) + str(ijList_u[i][1]) + "_car" + ".jpg"
				sting_full = out_img_path + "/" + out_img_file
				region_pil.save(out_img_path + "/" + out_img_file)
				title(sting_full)

	# axis('off')
	showBoxInSrc(pil_img_copy)
	# show()


