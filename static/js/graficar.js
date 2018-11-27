/*function graficarPalabrasRepetidas(canvas, data, labels, dataDos, labelsDos){
  var barChart = new Chart(canvas, {
    type: 'line',
    data: {
      datasets: [{
        label: 'Min ROC',
        fill: false,
        data: data,
        backgroundColor: 'red',
        labels: labels
      },
      {
        label: 'Max ROC',
        fill: false,
        data: dataDos,
        backgroundColor: 'grey',
        labels: labelsDos
      }]
    },
    options: {
        title: {
            display: true,
            text: 'Palabras más Repetidas'
        },
        scales: {
          xAxes: [{
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'Frecuencia'
              }
          }],
          yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Palabras'
              }
          }]

        }


    }
  });
  return barChart;
}*/

function graficarMaxCurve(canvas, data, labels){
  var barChart = new Chart(canvas, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Max ROC',
        fill: false,
        data: data,
        borderColor: "red"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
        title: {
            display: true,
            text: 'Curva de ROC Macro'
        },
        scales: {
          xAxes: [{
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'Tasa de Falsos Positivos'
              }
          }],
          yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Tasa de Verdaderos Positivos'
              },
              ticks: {
                min: 0,
                max: 1,
                stepSize: 0.1
              }
          }]

        }


    }
  });
  return barChart;
}

function graficarMinCurve(canvas, data, labels){
  var barChart = new Chart(canvas, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Min ROC',
        fill: false,
        data: data,
        borderColor: "blue"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
        title: {
            display: true,
            text: 'Curva de ROC Micro'
        },
        scales: {
          xAxes: [{
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'Tasa de Falsos Positivos'
              }
          }],
          yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Tasa de Verdaderos Positivos'
              },
              ticks: {
                min: 0,
                max: 1.0,
                stepSize: 0.1
              }
          }]

        }


    }
  });
  return barChart;
}

function graficarAcc(canvas, data, dataD, labels){
var myChart = new Chart(canvas, {
   type: 'line',
   data: {
     labels:labels,
     datasets: [{
       data: data,
       label: 'Acc',
       fill: false,
       backgroundColor: [
         'green'
       ]
     }, {
       data: dataD,
       label: 'Val_Acc',
       fill: false,
       backgroundColor: [
         'black'
       ]
     }, ]
   },
   options: {
     responsive: true,
     maintainAspectRatio: false,
     legend: {
       display: true,
     }
   }
 });
 return myChart;
}

function graficarLoss(canvas, data, dataD, labels){
var myChart = new Chart(canvas, {
   type: 'line',
   data: {
     labels:labels,
     datasets: [{
       data: data,
       label: 'Loss',
       fill: false,
       backgroundColor: [
         'green'
       ]
     }, {
       data: dataD,
       label: 'Val_Loss',
       fill: false,
       backgroundColor: [
         'black'
       ]
     }, ]
   },
   options: {
     responsive: true,
     maintainAspectRatio: false,
     legend: {
       display: true,
     }
   }
 });
 return myChart;
}




function graficarPruebaDos(canvas, data, dataD, labels){
var myChart = new Chart(canvas, {
   type: 'line',
   data: {
     labels:labels,
     datasets: [{
       data: data,
       fill: false,
       backgroundColor: [
         'green'
       ]
     }, {
       data: dataD,
       fill: false,
       backgroundColor: [
         'black'
       ]
     }, ]
   },
   options: {
     responsive: true,
     legend: {
       display: true,
     }
   }
 });
 return myChart;
}
