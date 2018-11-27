# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 09:39:52 2018

@author: Andres
"""

import numpy as np
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import load_model

from keras.utils import to_categorical

import time
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers import Activation
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
# Import Tensorflow with multiprocessing
import tensorflow as tf
import multiprocessing as mp

# Loading the CIFAR-10 datasets
from keras.datasets import cifar10
from keras.datasets import mnist
from keras import backend as K
from keras.datasets import fashion_mnist

def cargarDatos(opcionDataset):
    if (opcionDataset ==  'cifar'):
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    elif (opcionDataset == 'mnist'):
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
    else:
        (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

    return x_train, y_train, x_test, y_test

#a,b,c,d=cargarDatos('cifar')

def numeroClases(opcionDataset):
    if (opcionDataset ==  'cifar'):
        numeroClases=10
        class_names=['Avión','Auto','Ave' , 'Gato', 'Venado' , 'Perro' , 'Rana', 'Caballo', 'Bárco', 'Camión']
    elif (opcionDataset == 'mnist'):
        numeroClases=10
        class_names=['Cero','Uno','Dos' , 'Tres', 'Cuatro' , 'Cinco' , 'Seis', 'Siete', 'Ocho', 'Nueve']
    else:
        numeroClases=10
        class_names=['Camiseta', 'Pantalón', 'Jersey', 'Vestido', 'Abrigo', 'Sandalias', 'Camisa', 'Zapatillas', 'Bolso', 'Botines']

    return numeroClases, class_names

#e,f=numeroClases('cifar')

def procesarDatos(opcionDataset,x_train, y_train, x_test, y_test, num_classes):
    if (opcionDataset ==  'cifar'):
        y_train = np_utils.to_categorical(y_train, num_classes)
        y_test = np_utils.to_categorical(y_test, num_classes)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train  /= 255
        x_test /= 255
        input_shape=x_train.shape[1:]
    elif (opcionDataset == 'mnist'):
        if K.image_data_format() == 'channels_first':
            x_train = x_train.reshape(x_train.shape[0], 1, 28, 28)
            x_test = x_test.reshape(x_test.shape[0], 1, 28, 28)
            input_shape = (1, 28, 28)
        else:
            x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
            x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
            input_shape = (28, 28, 1)

        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255

        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)
    else:
        if K.image_data_format() == 'channels_first':
            x_train = x_train.reshape(x_train.shape[0], 1, 28, 28)
            x_test = x_test.reshape(x_test.shape[0], 1, 28, 28)
            input_shape = (1, 28, 28)
        else:
            x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
            x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
            input_shape = (28, 28, 1)

        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255

        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

    return x_train, y_train, x_test, y_test, input_shape

#g,h,i,j,k=procesarDatos('cifar',a,b,c,d,e)
