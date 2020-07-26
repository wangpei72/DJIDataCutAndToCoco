#!/usr/bin/env python
# coding: utf-8

import pandas as pd

import numpy as np
import scipy as sp
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Load Dataset 
mfccData = pd.read_csv("Frogs_MFCCs.csv")

# Get labels for classification
mfccData_ = mfccData.values[:, 1:22]

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
X = mfccData_
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

batch_size = 50
n_batch = len(X_train) // batch_size
INPUT_NODE = 21
LAYER1_NODE = 128
OUTPUT_NODE = 10
LEARNING_RATE_BASE = 0.01
LEARNING_RATE_DECAY = 0.99


def inference(input_tensor, weights1, biases1, weights2, biases2):
	layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)
	return tf.matmul(layer1, weights2) + biases2


# fcn
x = tf.compat.v1.placeholder(tf.float32, [None, 21])
y = tf.compat.v1.placeholder(tf.float32, [None, 10])
weights1 = tf.Variable(tf.random.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
biases1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]))
weights2 = tf.Variable(tf.random.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
biases2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))
pred = inference(x, weights1, biases1, weights2, biases2)

# loss & accuracy
cross_entropy = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=pred, labels=tf.argmax(y, 1)))
global_step = tf.Variable(0, trainable=False)
learning_rate = tf.compat.v1.train.exponential_decay(LEARNING_RATE_BASE, global_step,
                                                     n_batch, LEARNING_RATE_DECAY)
train = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step=global_step)
correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

import time

with tf.compat.v1.Session() as sess:
	start_time = time.perf_counter()
	sess.run(tf.compat.v1.global_variables_initializer())
	for epoch in range(20):
		for batch in range(n_batch):
			for i in range(batch_size):  # load batch
				rnd_indices = np.random.randint(0, len(X_train))
				x_b = X_train[rnd_indices]
				y_b = Y_train[rnd_indices]
				if i < 1:
					batch_xs = [x_b]
					batch_ys = [y_b]
				else:
					batch_xs = np.append(batch_xs, [x_b], axis=0)
					batch_ys = np.append(batch_ys, [y_b], axis=0)
			sess.run(train, feed_dict={x: batch_xs, y: batch_ys})
		if epoch % 5 == 0:
			acc = sess.run(accuracy, feed_dict={x: X_test, y: Y_test})
			print('Epoch' + str(epoch) + ',Testing Accuracy=' + str(acc))
	end_time = time.perf_counter()
	print('Running time:%s Second' % (end_time - start_time))  # 输出运行时间
	print('________')
	print('test show:')
	print('________')
	for i in range(5):
		rnd = np.random.randint(0, len(X))
		x_test = tf.compat.v1.placeholder(tf.float32, [1, 21])
		prediction = tf.argmax(inference(x_test, weights1, biases1, weights2, biases2), 1)
		print("input:")
		print(X[rnd])
		array = sess.run(prediction, feed_dict={x_test: [X[rnd]]})
		print("label:")
		print("Species : " + str(Species_class[array[0]]))
		print("prediction:")
		print("Family  : " + str(Species_Info[Y_[rnd]]['Family']))
		print("Genus   : " + str(Species_Info[Y_[rnd]]['Genus']))
		print("Species : " + str(Species_Info[Y_[rnd]]['Species']))
		print('\n\n')
