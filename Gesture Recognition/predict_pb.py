# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:49:42 2020

@author: Tanmay Thakur
"""
from keras import backend as K
import tensorflow as tf
from tensorflow.python.platform import gfile

sess = K.get_session()
graph_def = sess.graph.as_graph_def()

f = gfile.FastGFile("tf_model.pb", 'rb')
graph_def = tf.GraphDef()
# Parses a serialized binary message into the current message.
graph_def.ParseFromString(f.read())
f.close()

sess.graph.as_default()
# Import a serialized TensorFlow `GraphDef` protocol buffer
# and place into the current default `Graph`.
tf.import_graph_def(graph_def)

"""
Locate the input tensor so we can feed it with some input data and grab the predictions from the output tensor, we are going to get them by name. 
The only difference is that all tensors' names are prefixed with the string "import/" so the input tensor is now named "import/conv2d_1_input:0" and output tensor is "import/dense_2/Softmax:0"
"""

x_test ,output_tensor1, output_tensor2, x_1, x_2= "Symbolic test tensor"

# Single input/output
softmax_tensor = sess.graph.get_tensor_by_name('import/dense_2/Softmax:0')
predictions = sess.run(softmax_tensor, {'import/conv2d_1_input:0': x_test[:20]})

# Multiple input/output
predicts_1, predicts_2 = sess.run([output_tensor1, output_tensor2], {
    'import/input0:0': x_1[:20], 'import/input1:0': x_2[:20]})