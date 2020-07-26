#!/usr/bin/env python
# coding: utf-8

import pandas as pd
# import hvplot.pandas
import numpy as np
import scipy as sp
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

import time
import tensorflow as tf

# Load Dataset
mfccData = pd.read_csv("Frogs_MFCCs.csv")

# Get labels for classification
mfccData_data = mfccData.values[:, 1:22]

Family_class = np.unique(mfccData.values[:, 22]).tolist()
Genus_class = np.unique(mfccData.values[:, 23]).tolist()
Species_class = np.unique(mfccData.values[:, 24]).tolist()

total_num = len(mfccData.values)
Family_labels = np.zeros(total_num, dtype=np.int32)
Genus_labels = np.zeros(total_num, dtype=np.int32)
Species_labels = np.zeros(total_num, dtype=np.int32)
for i in range(total_num):
	Family_labels[i] = Family_class.index(mfccData.values[:, 22][i])
	Genus_labels[i] = Genus_class.index(mfccData.values[:, 23][i])
	Species_labels[i] = Species_class.index(mfccData.values[:, 24][i])

X = mfccData_data
Y_ = Species_labels

Species_Info = [
	{'Family': 'Leptodactylidae', 'Genus': 'Adenomera', 'Species': 'AdenomeraAndre'},
	{'Family': 'Leptodactylidae', 'Genus': 'Adenomera', 'Species': 'AdenomeraHylaedactylus'},
	{'Family': 'Dendrobatidae', 'Genus': 'Ameerega', 'Species': 'Ameeregatrivittata'},
	{'Family': 'Hylidae', 'Genus': 'Dendropsophus', 'Species': 'HylaMinuta'},
	{'Family': 'Hylidae', 'Genus': 'Hypsiboas', 'Species': 'HypsiboasCinerascens'},
	{'Family': 'Hylidae', 'Genus': 'Hypsiboas', 'Species': 'HypsiboasCordobae'},
	{'Family': 'Leptodactylidae', 'Genus': 'Leptodactylus', 'Species': 'LeptodactylusFuscus'},
	{'Family': 'Hylidae', 'Genus': 'Osteocephalus', 'Species': 'OsteocephalusOophagus'},
	{'Family': 'Bufonidae', 'Genus': 'Rhinella', 'Species': 'Rhinellagranulosa'},
	{'Family': 'Hylidae', 'Genus': 'Scinax', 'Species': 'ScinaxRuber'},
]

Y = np.eye(10)[Y_]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)

# 一个batch中训练数据的个数
batch_size = 55
# //运算符取整数
n_batch = len(X_train) // batch_size
# 输入层的节点数
INPUT_NODE = 21
# 隐藏层节点数
LAYER_NODE = 128
# 输出层的节点数--类别的数目
OUTPUT_NODE = 10
# 基础的学习率
LEARNING_RATE_BASE = 0.1
# 学习率的衰减率
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001


# 一个辅助函数,给定网络的输入和所有参数,计算网络的前向传播结果
# relu函数 三层全连接网络
def inference(input_tensor, weights1, biases1, weights2, biases2):
	layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)
	return tf.matmul(layer1, weights2) + biases2


# 这里没有设置滑动平均参数

# 单层隐藏层
x = tf.compat.v1.placeholder(tf.float32, [None, INPUT_NODE], name='x-input')
y_ = tf.compat.v1.placeholder(tf.float32, [None, OUTPUT_NODE], name='y-input')

# 生成隐藏层参数 正太分布
weights1 = tf.Variable(
	tf.random.truncated_normal([INPUT_NODE, LAYER_NODE], stddev=0.1)
)
biases1 = tf.Variable(
	tf.constant(0.1, shape=[LAYER_NODE])
)
# 生成输出层的参数
weights2 = tf.Variable(
	tf.random.truncated_normal([LAYER_NODE, OUTPUT_NODE], stddev=0.1)
)
biases2 = tf.Variable(
	tf.constant(0.1, shape=[OUTPUT_NODE])
)
# 预测值
y = inference(x, weights1, biases1, weights2, biases2)
# 代表寻来你轮数的变量被设置为不可训练的参数
global_step = tf.Variable(0, trainable=False)
cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
	logits=y, labels=tf.argmax(y_, 1)
)
cross_entropy_mean = tf.reduce_mean(cross_entropy)
# 设定损失函数
loss = cross_entropy_mean
# 设定学习率
learning_rate = tf.compat.v1.train.exponential_decay(
	LEARNING_RATE_BASE,  # 基础学习率
	global_step,  # 当前迭代轮数
	n_batch,  # 过完所有的训练数据迭代次数
	LEARNING_RATE_DECAY  # 学习率衰减速率
)

train = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
# 一组数据上的准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
	start_time = time.perf_counter()
	tf.global_variables_initializer().run()
	for epoch in range(200):
		for batch in range(n_batch):
			for i in range(batch_size):
				rnd_ = np.random.randint(0, len(X_train))
				x_b = X_train[rnd_]
				y_b = Y_train[rnd_]
				if i < 1:
					batch_xs = [x_b]
					batch_ys = [y_b]
				else:
					batch_xs = np.append(batch_xs, [x_b], axis=0)
					batch_ys = np.append(batch_ys, [y_b], axis=0)
			sess.run(train, feed_dict={x: batch_xs, y_: batch_ys})
		if epoch % 5 == 0:
			accuracy_ = sess.run(accuracy, feed_dict={x: X_test, y_: Y_test})
			print('epoch ' + str(epoch) + ' test accuracy is: ' + str(accuracy_))
	end_time = time.perf_counter()
	print('Running time: %s  secs' % (end_time - start_time))
	print('*****test show:')
	for i in range(5):
		rnd = np.random.randint(0, len(X))
		x_test = tf.compat.v1.placeholder(tf.float32, [1, 21])
		prediction = tf.argmax(inference(x_test, weights1, biases1, weights2, biases2), 1)
		print("input:")
		print(X[rnd])
		array = sess.run(prediction, feed_dict={x_test: [X[rnd]]})
		print("label:")
		print("Species : " + str(Species_class[array[0]]))
		print("Family : " + str(Species_Info[Y_[rnd]]['Family']))
		print("Genus : " + str(Species_Info[Y_[rnd]]['Genus']))
		print("Species : " + str(Species_Info[Y_[rnd]]['Species']))
		print('\n\n\n')
