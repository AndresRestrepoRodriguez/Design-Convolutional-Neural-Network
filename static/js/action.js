$(document).ready(function() {
  var popCanvas = $("#popChart");
  var popCanvasDos = $("#popChartDos");
  var popCanvasTres = $("#popChartTres");
  var popCanvasCuatro = $("#popChartCuatro");
  var contadorConv2d=0;
  var yMicro;
  var xMicro;
  var yMacro;
  var xMacro;
  var acc;
  var val_acc;
  var lossD;
  var val_loss;
  var labelsAcc=[];
  var labelsLoss=[];
  var canvasEmpty;
  var dataURLEmpty;
  var contadorConvolucion=0;


  $( "#btnAddConv" ).click(function() {
    if (!$('#filters').val()){
      swal({
            title: "Oops!",
            text: "No dejes el espacio en blanco",
            icon: "warning"
          });
    }
    else{
      contadorConvolucion = contadorConvolucion + 1;
      contadorConv2d = contadorConv2d + 1;
          pal="conv2d,";
          pal+=$('#filters').val();
          pal+=",";
          pal+=$('#padding').val();
          pal+=",";
          pal+=$('#activation').val();
        $('#terminosAgregados').append($('<option>', {
            value: pal,
            text : pal
        }));
    }

  });

  $( "#btnAddPooling" ).click(function() {
    if (!$('#dimensionUno').val() || !$('#dimensionDos').val()){
      swal({
            title: "Oops!",
            text: "No dejes el espacio en blanco",
            icon: "warning"
          });
    } else if (contadorConvolucion == 0){
      swal({
            title: "Oops!",
            text: "Debes agregar primero una capa de convolución",
            icon: "warning"
          });
    }
    else{
      pal="maxpooling2d,";
      palDos="maxpooling2d,";
      pal+="(";
      pal+=$('#dimensionUno').val();
      palDos+=$('#dimensionUno').val();
      pal+=",";
      palDos+=",";
      pal+=$('#dimensionDos').val();
      palDos+=$('#dimensionDos').val();
      pal+=")";
      $('#terminosAgregados').append($('<option>', {
          value: palDos,
          text : pal
      }));
    }


  });


  $( "#btnAddDropout" ).click(function() {
    if (!$('#rate').val()){
      swal({
            title: "Oops!",
            text: "No dejes el espacio en blanco",
            icon: "warning"
          });
    }else if (contadorConvolucion == 0){
      swal({
            title: "Oops!",
            text: "Debes agregar primero una capa de convolución",
            icon: "warning"
          });
    }
    else{
      pal="dropout,";
      pal+=$('#rate').val();

      $('#terminosAgregados').append($('<option>', {
          value: pal,
          text : pal
      }));

    }

  });

  $( "#btnAddDense" ).click(function() {
    if (!$('#units').val()){
      swal({
            title: "Oops!",
            text: "No dejes el espacio en blanco",
            icon: "warning"
          });
    }else if (contadorConvolucion == 0){
      swal({
            title: "Oops!",
            text: "Debes agregar primero una capa de convolución",
            icon: "warning"
          });
    }
    else{
      pal="dense,";
      pal+=$('#units').val();
      pal+=",";
      pal+=$('#activacion').val();
      $('#terminosAgregados').append($('<option>', {
          value: pal,
          text : pal
      }));

    }


  });

  $( "#btnAddOpt" ).click(function() {
      console.log('opt');
      pal=$('#optimizer').val();
      $('#terminosAgregados').append($('<option>', {
          value: pal,
          text : pal
      }));

  });

  $( "#btnAddLoss" ).click(function() {
      pal=$('#loss').val();
      $('#terminosAgregados').append($('<option>', {
          value: pal,
          text : pal
      }));

  });

  $( "#btnAddMetric" ).click(function() {
      pal=$('#metric').val();
      $('#terminosAgregados').append($('<option>', {
          value: pal,
          text : pal
      }));

  });

  $( "#btnAddFlatten" ).click(function() {
    if (contadorConvolucion == 0){
      swal({
            title: "Oops!",
            text: "Debes agregar primero una capa de convolución",
            icon: "warning"
          });
    }else{
      pal="flatten";
      $('#terminosAgregados').append($('<option>', {
          value: pal,
          text : pal
      }));

    }

  });

$('#contact').css("display", "none");
$('#contactInicio').css("display", "none");

  $( "#btnDelete" ).click(function() {
    if( !$('#terminosAgregados').has('option').length > 0 ){
        swal({
              title: "Oops!",
              text: "No ingresaste términos para la búsqueda",
              icon: "error"
            });
      }
      else if(!$('#epocs').val() || !$('#batch').val()){
        swal({
              title: "Oops!",
              text: "No ingresaste batch o epocs o ambos",
              icon: "error"
            });
      }
      else{
        $('#contactForm').fadeToggle();
        var values = $("#terminosAgregados>option").map(function() { return $(this).val(); });
        var longitudTerminos=values.length;
        var batch_size=$('#batch').val();
        var epocs=$('#epocs').val();
        var opti=$('#optimizer').val();
        var lossF=$('#loss').val();
        var metrica=$('#metric').val();
        var tipoDataset = $("input[name='optradio']:checked").val();
        var i;
        var jsonFinal='{ ';
        for (i = 0; i < longitudTerminos; i++) {
            if (i < (longitudTerminos-1)){
              jsonFinal+='"'+i+'" : '+'"'+values[i]+'" , ';
            }
            else{
              jsonFinal+='"'+i+'" : '+'"'+values[i]+'" ,';
            }
          }
          jsonFinal+='"'+(i++)+'" : '+'"'+opti+'" , '+'"'+(i++)+'" : '+'"'+lossF+'" , '+'"'+(i++)+'" : '+'"'+metrica+'" ,';
          jsonFinal+='"'+(i++)+'" : '+'"'+batch_size+'" , '+'"'+(i++)+'" : '+'"'+epocs+'" ,  '+'"'+(i++)+'" : '+'"'+tipoDataset+'" ';
          jsonFinal+=' }';

          var obj = JSON.parse(jsonFinal);
          console.log(obj)
          $("#terminosAgregados").empty();
          $.ajax({
        			data : obj,
        			type : 'POST',
        			url : '/process'
      		  })
            .done(function(data) {

        			if (data.error) {
                console.log(data.error);
                $('#contactForm').fadeToggle();
        			}
        			else {

                $('#zonaAnalisis').show();
                loss=data.loss;
                metric=data.metric;
                $('#funcionLoss').text('Loss : '+loss);
                $('#funcionMetrics').text('Accuracy : '+metric);


                yMicro=data.tprMicro;
                xMicro=data.fprMicro;
                yMacro=data.tprMacro;
                xMacro=data.fprMacro;

                console.log(yMicro);
                console.log(xMicro);
                console.log(yMacro);
                console.log(xMacro);

                const dataMicro = xMicro.map((x, i) => {
                return {
                  x: x.toFixed(2),
                  y: yMicro[i].toFixed(2)
                };
              });

              const dataMacro = xMacro.map((x, i) => {
              return {
                x: x.toFixed(2),
                y: yMacro[i].toFixed(2)
              };
            });

              console.log(dataMicro);
              console.log(dataMacro);
              console.log(typeof(xMacro[0]));

              acc = data.acc;
              val_acc = data.val_acc;
              lossD = data.lossD;
              val_loss = data.val_loss;
              labelsAcc=[];
              labelsLoss=[];

              for (paso = 0; paso < acc.length; paso++) {
                labelsAcc[paso] = paso.toFixed(1);
              };

              for (paso = 0; paso < lossD.length; paso++) {
                labelsLoss[paso] = paso.toFixed(1);
              };

               $('#contactForm').fadeToggle();
                $('#visualizacionModelo').append("<img id='mo' src='/static/images/model.png' class='img-responsive img-fluid center-block'>");
                //<img id="lgF" src="/static/images/Escudo_UD.png" alt="img caron" class="img-responsive img-fluid center-block">
                graficoUno=graficarMaxCurve(popCanvas, data.tprMacro, data.fprMacro);
                //graficoUno=graficarPruebaDos(popCanvas, dataMicro, dataMacro, xMicro)
                graficoDos=graficarMinCurve(popCanvasDos,data.tprMicro ,data.fprMicro);
                graficaTres=graficarLoss(popCanvasTres,acc, val_acc, labelsAcc);
                graficaCuatro=graficarAcc(popCanvasCuatro,lossD, val_loss, labelsLoss);
                $('#zonaPrediccion').show();
                canvasEmpty = document.getElementById('popChartCinco');
                dataURLEmpty = canvasEmpty.toDataURL();
                $('#zonaDescarga').show();
              }
        		  });
      }


          event.preventDefault();
  });

  $('[data-toggle="tooltip"]').tooltip();

  $( "#downloadCompendioLoss" ).click(function() {
  var contenidoDeArchivo = "Compendio de Datos";
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'Datos Gráfica de Función de Pérdida'
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'loss : '+lossD;
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'val_loss : '+val_loss;
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'ejeY : '+labelsLoss;
  contenidoDeArchivo += '\n';

  console.log(contenidoDeArchivo);

  var elem = document.getElementById('desCompendioLoss');

  elem.download = "archivo.txt";
  elem.href = "data:application/octet-stream,"
                       + encodeURIComponent(contenidoDeArchivo);
 elem.click();

  });

  $( "#downloadCompendioMet" ).click(function() {
  var contenidoDeArchivo = "Compendio de Datos";
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'Datos Gráfica de Métrica'
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'acc : '+acc;
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'val_acc : '+val_acc;
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'ejeY : '+labelsAcc;

  console.log(contenidoDeArchivo);

  var elem = document.getElementById('desCompendioMet');

  elem.download = "archivo.txt";
  elem.href = "data:application/octet-stream,"
                       + encodeURIComponent(contenidoDeArchivo);
 elem.click();

  });

  $( "#downloadCompendioCMicro" ).click(function() {
  var contenidoDeArchivo = "Compendio de Datos";
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'Curva de ROC MICRO'
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'ejeX : '+xMicro;
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'ejeY : '+yMicro;

  console.log(contenidoDeArchivo);

  var elem = document.getElementById('desCompendioCMicro');

  elem.download = "archivo.txt";
  elem.href = "data:application/octet-stream,"
                       + encodeURIComponent(contenidoDeArchivo);
 elem.click();

  });

  $( "#downloadCompendioCMacro" ).click(function() {
  var contenidoDeArchivo = "Compendio de Datos";
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'Curva de ROC MACRO'
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'ejeX : '+xMacro;
  contenidoDeArchivo += '\n';
  contenidoDeArchivo += 'ejeY : '+yMacro;
  console.log(contenidoDeArchivo);

  var elem = document.getElementById('desCompendioCMacro');

  elem.download = "archivo.txt";
  elem.href = "data:application/octet-stream,"
                       + encodeURIComponent(contenidoDeArchivo);
 elem.click();

  });

  $( "#downloadModelo" ).click(function() {
  var elem = document.getElementById('desModelo');
  elem.click();

  });


  $( "#btnEnviarImagen" ).click(function() {
     var canvas = document.getElementById('popChartCinco');
     var dataURL = canvas.toDataURL();
     console.log(dataURL);
     if(dataURL == dataURLEmpty){
       swal({
             title: "Oops!",
             text: "Debes adjuntar una imagen",
             icon: "error"
           });
     }else{
       var jsonF = '{';
       jsonF += '"'+1+'" : '+'"'+dataURL+'" ';
       jsonF += '}';
       var obj = JSON.parse(jsonF);
       console.log(obj);
       $.ajax({
           data : obj,
           type : 'POST',
           url : '/processIma'
         })
        .done(function(data) {

           if (data.error) {
             console.log(data.error);
           }
           else {
             console.log(data.y);
             $('#textoPrediccion').text(data.y);
           }
           });
     }

         event.preventDefault();


  });

  $( "#downloadCanvasUno" ).click(function() {
        formatoUno=$("#formatoUno").val();
        download_image("popChart",formatoUno);
      });

  $( "#downloadCanvasDos" ).click(function() {
        formatoDos=$("#formatoDos").val();
        download_image("popChartDos",formatoDos);
      });

  $( "#downloadCanvasTres" ).click(function() {
        formatoTres=$("#formatoTres").val();
        download_image("popChartTres",formatoDos);
      });

  $( "#downloadCanvasCuatro" ).click(function() {
        formatoCuatro=$("#formatoCuatro").val();
        download_image("popChartCuatro",formatoDos);
      });

});

function upload(){
  var imgcanvas = document.getElementById("popChartCinco");
  var fileinput = document.getElementById("fininput");
  var filename = fileinput.value;
  //alert("Chose "+ filename);
  var image = new SimpleImage(fileinput);
  console.log(typeof(image))

  image.drawTo(imgcanvas);
}
