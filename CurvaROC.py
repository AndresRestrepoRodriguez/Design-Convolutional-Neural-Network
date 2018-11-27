# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:55:21 2018

@author: Andres
"""

from sklearn.datasets import make_classification
from sklearn.preprocessing import label_binarize
from scipy import interp
from itertools import cycle
from sklearn.metrics import roc_curve, auc
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
from keras.utils import plot_model

from keras.utils import to_categorical


def scnn(model, test_data):
    scnn_pred = model.predict(test_data, batch_size=3, verbose=1)
    scnn_predicted = np.argmax(scnn_pred, axis=1)
    return scnn_pred, scnn_predicted

#a, b = scnn(model, test_data)

def generarDicts(n_classes, test_labels_one_hot, scnn_pred):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(test_labels_one_hot[:, i], scnn_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    return fpr, tpr, roc_auc


#c ,d ,e = generarDicts(3,test_labels_one_hot,a)

# Compute micro-average ROC curve and ROC area
def compuMicro(fpr, tpr, roc_auc, test_labels_one_hot, scnn_pred):
    fpr["micro"], tpr["micro"], _ = roc_curve(test_labels_one_hot.ravel(), scnn_pred.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    print(roc_auc["micro"])
    return fpr["micro"], tpr["micro"] , roc_auc["micro"]

#f , g , h =compuMicro(c,d,e,test_labels_one_hot, a)


def generarAllMean(fpr, tpr, n_classes):
    # First aggregate all false positive rates
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])

    # Finally average it and compute AUC
    mean_tpr /= n_classes
    return all_fpr, mean_tpr


#i, j= generarAllMean(c, d,3)

def generarMacro(all_fpr, mean_tpr, fpr, tpr, roc_auc):
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    return roc_auc["macro"], fpr["macro"], tpr["macro"]

#k , m , n =generarMacro(i,j,c,d,e)

def convertirLista(fprMicro, tprMicro, fprMacro, tprMacro):
    fprMicro = fprMicro.tolist()
    tprMicro = tprMicro.tolist()
    fprMacro = fprMacro.tolist()
    tprMacro = tprMacro.tolist()
    return fprMicro, tprMicro, fprMacro, tprMacro

def definirMetrica(metric):
    if metric == 'accuracy':
        met='acc'
        metrica='val_acc'
    else:
        met='mean_squared_error'
        metrica='val_mean_squared_error'
    return met, metrica


def valoresLossMetrics(hist, met, val_metrica):
    return hist.history[met], hist.history[val_metrica], hist.history['loss'], hist.history['val_loss']
