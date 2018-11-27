from flask import Flask, render_template, request, jsonify
import Datos as lpi
import FuncionesModelo as pk
import CurvaROC as cr
from io import BytesIO
import base64
import re
import json
from PIL import Image
import numpy as np

app = Flask(__name__)
global dataset
global name_clases

@app.route('/')
def index():
	return render_template('principal.html')

@app.route('/manuales')
def manuales():
	return render_template('manuales.html')


@app.route('/process', methods=['POST'])
def process():
    global dataset
    global name_clases
    global modelo
    parametros=[]
    contenido = request.form
    diccionarioContenido=contenido.copy()
    print(diccionarioContenido)
    for i in range(len(diccionarioContenido)):
        parametros.append(diccionarioContenido[str(i)])
    print(parametros)

    #parametros=['conv2d,32,same,relu', 'conv2d,32,same,relu', 'maxpooling2d,2,2', 'dropout,0.25', 'conv2d,64,same,relu', 'conv2d,64,same,relu', 'maxpooling2d,2,2', 'dropout,0.25', 'conv2d,64,same,relu', 'conv2d,64,same,relu', 'maxpooling2d,2,2', 'dropout,0.25', 'flatten', 'dropout,0.5',  'rmsprop', 'categorical_crossentropy', 'accuracy','5', '5']

    dataset=parametros.pop()
    epocs=parametros.pop()
    batch_size=parametros.pop()
    metrics=parametros.pop()
    loss=parametros.pop()
    optimizer=parametros.pop()
    #dataTraining, dataTrainingLabels=lpi.dataTraining()
    #dataTest, dataTestLabels=lpi.dataTest()
    #numClases=lpi.numeroClases(dataTrainingLabels)
    #train_data, train_data_labels, test_data, test_data_labels, input_shape = lpi.dataReshape(dataTraining, dataTest, dataTrainingLabels , dataTestLabels)

    dataTraining, dataTrainingLabels, dataTest, dataTestLabels = lpi.cargarDatos(dataset)
    numClases, name_clases=lpi.numeroClases(dataset)
    train_data, train_data_labels, test_data, test_data_labels, input_shape = lpi.procesarDatos(dataset, dataTraining, dataTrainingLabels, dataTest , dataTestLabels, numClases)




    modelo=pk.iniciarModelo()
    modelo=pk.generarModelo(parametros, modelo,numClases, input_shape)
    modelo=pk.compilarModelo(optimizer, loss, metrics, modelo)
    modelo, history=pk.fitModel(modelo, train_data, train_data_labels, epocs, batch_size ,test_data, test_data_labels)
    pk.plotModel(modelo)
    loss, metricsD = pk.evaluateModel(modelo, test_data,test_data_labels)
    scnn_pred, scnn_predicted = cr.scnn(modelo, test_data)
    fpr, tpr, roc_auc = cr.generarDicts(numClases, test_data_labels, scnn_pred)
    fprMicro, tprMicro, rocMicro = cr.compuMicro(fpr, tpr, roc_auc, test_data_labels, scnn_pred)
    all_fpr, mean_tpr = cr.generarAllMean(fpr, tpr, numClases)
    rocMacro, fprMacro, tprMacro = cr.generarMacro(all_fpr, mean_tpr, fpr, tpr, roc_auc)
    fprMicro, tprMicro, fprMacro, tprMacro = cr.convertirLista(fprMicro, tprMicro, fprMacro, tprMacro)
    met, metri = cr.definirMetrica(metrics)
    acc, val_acc, lossD, val_loss = cr.valoresLossMetrics(history, met, metri)
    print(acc)
    print(val_acc)
    print(lossD)
    print(val_loss)

    if (contenido) :
        parametros=[]
        return jsonify({ 'loss' :  loss , 'metric' :  metricsD, 'fprMicro' : fprMicro, 'tprMicro' : tprMicro , 'fprMacro' : fprMacro, 'tprMacro' : tprMacro, 'acc' : acc, 'val_acc' : val_acc , 'lossD' : lossD, 'val_loss' : val_loss })
    else:
        parametros=[]
        return jsonify({'error' : 'Los términos no arrojaron resultados!'})

@app.route('/processIma', methods=['POST'])
def processIma():
    image_data = re.sub('^data:image/.+;base64,', '', request.form['1'])
    im = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
    print(im)
    #sim.show()
    open_cv_image = np.array(im)
    print(open_cv_image)
    print(open_cv_image.shape)
    #contenido = request.form
    #diccionarioC=contenido.copy()
    #print(diccionarioC)
    print(dataset)
    resultado=pk.prediccion(open_cv_image,dataset,name_clases,modelo)
    if (im) :
        parametros=[]
        return jsonify({ 'y' :  resultado  })
    else:
        parametros=[]
        return jsonify({'error' : 'Los términos no arrojaron resultados!'})

if __name__ == '__main__':
	app.run(debug=False)
