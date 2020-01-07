# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 10:14:36 2019

@author: Unnikrishnan Menon
"""

from keras.models import Sequential, Model, model_from_json
from keras.layers import Dense, Conv2D, Activation, MaxPool2D, Flatten, Dropout, BatchNormalization
from keras.utils import np_utils
from keras.models import load_model
import pandas as pd
import numpy as np


data=pd.read_csv('fer2013/fer2013.csv')

data.head()

train = data[["emotion", "pixels"]][data["Usage"] == "Training"]
train['pixels'] = train['pixels'].apply(lambda im: np.fromstring(im, sep=' '))
x_train = np.vstack(train['pixels'].values)
y_train = np.array(train["emotion"])

x_train = x_train.reshape(-1, 48, 48, 1)

test = data[["emotion", "pixels"]][data["Usage"] == "PublicTest"]
test['pixels'] = test['pixels'].apply(lambda im: np.fromstring(im, sep=' '))
x_test = np.vstack(test['pixels'].values)
y_test = np.array(test["emotion"])

x_test = x_test.reshape(-1, 48, 48, 1)

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

model = Sequential()
model.add(Conv2D(64, 3, input_shape=(48, 48, 1)))
model.add(BatchNormalization())
model.add(Activation("relu"))

model.add(Conv2D(64, 3))
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))
model.add(Dropout(0.6))

model.add(Conv2D(32, 3))
model.add(BatchNormalization())
model.add(Activation("relu"))

model.add(Conv2D(32, 3))
model.add(BatchNormalization())
model.add(Activation("relu"))

model.add(Conv2D(32, 3))
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))
model.add(Dropout(0.6))

model.add(Flatten())
model.add(Dense(128))
model.add(BatchNormalization())
model.add(Activation("relu"))
model.add(Dropout(0.6))

model.add(Dense(7))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

model.fit(x_train,y_train,batch_size=100,epochs=10)

model.save('my_model.hdf5')
