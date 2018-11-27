# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 12:22:50 2018

@author: Andres
"""

import numpy as np
from keras.preprocessing import image
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras.utils import plot_model
import cv2
import numpy as np

# iniciar el modelo como secuencial
def iniciarModelo():
    model = Sequential()
    return model

#re=iniciarModelo()
#print(re)

# Funciones para añadir las  cinco capas
def add_conv2dInicial(filters, padding, activation, model, input_shape):
    filters=int(filters)
    model.add(Conv2D(filters, (3, 3),input_shape=input_shape, padding=padding, activation=activation))

# Funciones para añadir las  cinco capas
def add_conv2dSinPadding(filters, activation, model, input_shape):
    filters=int(filters)
    model.add(Conv2D(filters, (3, 3),input_shape=(3, 32, 32), activation=activation))

def add_conv2d(filters, padding, activation, model):
    filters=int(filters)
    model.add(Conv2D(filters, (3, 3), padding=padding, activation=activation))

def add_maxPooling2d(uno, dos, model):
    uno=int(uno)
    dos=int(dos)
    model.add(MaxPooling2D(pool_size=(uno, dos)))

def add_dropout(rate, model):
    rate=float(rate)
    model.add(Dropout(rate))

def add_dense(units, activation, model):
    units=int(units)
    model.add(Dense(units, activation=activation))

def add_flatten(model):
    model.add(Flatten())


def convStringToArray(cadena):
    arrayTerminos=cadena.split(",")
    return arrayTerminos

#sd=convStringToArray('conv2d')
#print(sd)

#arr=['conv2d,32,same,relu', 'conv2d,32,same,relu', 'maxpooling2d,2,2', 'dropout,0.25', 'conv2d,64,same,relu', 'conv2d,64,same,relu', 'maxpooling2d,2,2', 'dropout,0.25', 'conv2d,64,same,relu', 'conv2d,64,same,relu', 'maxpooling2d,2,2', 'dropout,0.25', 'flatten', 'dropout,0.5']

def generarModelo(arregloTerminos, model, nClasses, input_shape):
    arrayTemp=[]
    modelR=model
    contador=0
    for i in range(len(arregloTerminos)):
        arrayTemp=convStringToArray(arregloTerminos[i])
        tipoCapa=arrayTemp[0]
        if (tipoCapa == 'conv2d'):
            if contador>0:
                print('conv2d')
                add_conv2d(arrayTemp[1],arrayTemp[2],arrayTemp[3],modelR)
            else:
                print('conv2d')
                add_conv2dInicial(arrayTemp[1],arrayTemp[2],arrayTemp[3],modelR, input_shape)
            contador=contador+1
        elif (tipoCapa == 'maxpooling2d'):
            print('maxpooling2d')
            add_maxPooling2d(arrayTemp[1],arrayTemp[2],modelR)
        elif (tipoCapa == 'dropout'):
            print('dropout')
            add_dropout(arrayTemp[1],modelR)
        elif (tipoCapa == 'dense'):
            print('dense')
            add_dense(arrayTemp[1],arrayTemp[2], modelR)
        else:
            print('flatten')
            add_flatten(modelR)
    modelR.add(Dense(nClasses, activation='softmax'))
    return modelR

#a=generarModelo(arr, iniciarModelo(),3)

def compilarModelo(opt, loss, metrics, model):
    model.compile(optimizer=opt, loss=loss, metrics=[metrics])
    model.summary()
    return model

#a.summary()

#b=compilarModelo('rmsprop','categorical_crossentropy','accuracy',a)
#b.summary()

def fitModel(model, train_data, train_labels_one_hot, epochs, batch_size, test_data, test_labels_one_hot):
    epochs=int(epochs)
    batch_size=int(batch_size)
    history=model.fit(train_data, train_labels_one_hot,epochs=epochs ,batch_size=batch_size, verbose=1, validation_data=(test_data, test_labels_one_hot))
    model.save('D:/Users/Andres/Documents/Vera/productoCNN/static/modelo.h5')
    return model, history

def evaluateModel(model,testData, testDataLabels):
    modelT=model.evaluate(testData, testDataLabels)
    return modelT[0], modelT[1]
    #print(evaluate[0])
    #print(evaluate[1])

def plotModel(model):
    plot_model(model, to_file='D:/Users/Andres/Documents/Vera/productoCNN/static/images/model.png')

def prediccion(image, opcionDataset, name_array, model):
    #model=load_model('D:/Users/Andres/Documents/Vera/productoCNN/static/modelo.h5')
    if (opcionDataset ==  'cifar'):
        res = cv2.resize(image, dsize=(32,32), interpolation=cv2.INTER_CUBIC)
        test_imageU = np.expand_dims(res, axis = 0)
    elif (opcionDataset == 'mnist'):
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        res = cv2.resize(gray, dsize=(28,28), interpolation=cv2.INTER_CUBIC)
        test_imageU = np.expand_dims(res, axis = 0)
        test_imageU = np.expand_dims(test_imageU, axis = 3)
    else:
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        res = cv2.resize(gray, dsize=(28,28), interpolation=cv2.INTER_CUBIC)
        test_imageU = np.expand_dims(res, axis = 0)
        test_imageU = np.expand_dims(test_imageU, axis = 3)

    noj=model.predict_classes(test_imageU)
    classname = noj[0]
    print("Class: ",classname)
    print(name_array[classname])

    return name_array[classname]
