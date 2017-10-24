index = {

	init : function(){
		this.Form();

	},
	Form:function(){
		$("#mun").select2({  
		  	placeholder: "Seleccionar Municipio",
			allowClear: true
		});
		$("#carg").select2({  
			placeholder: "Seleccionar Cargo",
			allowClear: true
		});
		$("#multiple").multipleSelect({  
			placeholder: "Seleccionar Contactos",
			filter: true,
			width: '100%'		
		});
		$("#fakeLoader").fakeLoader({
			timeToHide:1500, 
			zIndex:"999",
			spinner:"spinner7",
			bgColor:"#009688"
		});		
			
		$("#mun").bind().change(function(){			
			var mun = $("#mun").val();
			$.ajax({
				type: 'GET',		
				url: '../default/index',						
				data: {mun},
			})
			.done(function(respuesta) {
				var respuesta = JSON.parse(respuesta);								
				$.each(respuesta, function(i, item) {					  				
    				$("#carg").append($("<option></option>").val(respuesta[i].id).html(respuesta[i].descripcion));
				});										
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
		});

		$("#carg").bind().change(function(){
			var mun = $("#mun").val();
			var carg = $("#carg").val();
			$.ajax({
				url: '../default/index',
				type: 'GET',				
				data: {carg,
					   mun},
			})
			.done(function(numeros) {
				var numeros = JSON.parse(numeros);				
				$.each(numeros, function(i, item) {					  				
    				$("#multiple").append($("<option></option>").val(numeros[i].numero).html(numeros[i].numero));
				});	
				$("#multiple").multipleSelect();

			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
			
		});

		$('#formSms').submit(function(e){
        	e.preventDefault();
        	return false;
         });
		
		$('#guardar').click(function(){
			if($('#formSms')[0].checkValidity()){
				var mun = $("#mun").val();
				var carg = $("#carg").val();
				var mensaje = $("#mensaje").val();					
				var celulares = $("#multiple").val();		
				$.ajax({
					url: '../enviar/guardarMensaje',
					type: 'POST',
					dataType: 'json',
					data: {celulares,
						   mun,
						   carg,
						   mensaje},
				})
				.done(function(respuesta) {					
					swal({
	  					title: 'Guardando mensajes.!',
	  					type: 'success',
	  					timer: 5000,	  					
						html: $('<div>')
						.addClass('some-class')
						.text('En breve sus mensajes seran encolado')
						})
					    url = '../default/index';
					    setTimeout(function(){  $( location ).attr("href", url); }, 2000);
				})
				.fail(function() {
					console.log("error");
				})
				.always(function() {

				});
			}	

		});
		var text_max = 160;
		$('#contandoCaracteres').html(text_max + ' caracteres');
		$('#mensaje').bind().keyup(function() {
		  $("#contandoCaracteres").empty();
		  var text_length = $('#mensaje').val().length;
		  var text_remaining = text_max - text_length;		  
		  $('#contandoCaracteres').html(text_remaining + ' restantes');
		});

		$('#enviar').bind().click(function(){
			
			if ($('#enviar').val() > 0) {
				swal({
					title: "¿Desea enviar" + $('#enviar').val() + "mensajes?",
					text: "Seran enviados los mensajes en cola",
					type: "warning",
					showCancelButton: true,
					confirmButtonColor: "#009688",
					confirmButtonText: "Enviar",
					cancelButtonText: "Cancelar",
					closeOnConfirm: false,
					closeOnCancel: false,
					cancelButtonText: 'Cancelar',
					customClass: "maskSweet",
				}).then(function(isConfirm){					
					if (isConfirm) {						
						$.ajax({
							type: "GET",
							url: '../enviar/enviarMensaje',
							dataType: 'json',
						}).done(function(respuesta) {
							if (respuesta.estatus == 200){
																													
								swal({
									title: respuesta.data,
									text: "...",
									type: "success",
									showConfirmButton :false,
									timer: 3000,
									customClass: "maskSweet"
								})
								url = '../default/index';
					    		setTimeout(function(){  $( location ).attr("href", url); }, 3000);
							}
							else{
								swal({
									title: "Hubo un problema",
									text: respuesta,
									type: "warning",
									showConfirmButton :false,
									timer: 3000,
									customClass: "maskSweet"
								})
								url = '../default/index';
					    		setTimeout(function(){  $( location ).attr("href", url); }, 3000);

							}

						});

					} else {
						swal({
							title: "Cancelado",
							text: "No se ha eliminado su articulo del carrito.",
							type: "error",
							customClass: "maskSweet"
						})
					}
				})
			
			}

			else{
					swal({
						title: "No hay mensajes en el buzon!",
						text: "Guarde un mensaje, luego envielo...!.",
						type: "error",
						customClass: "maskSweet"
						})
				}















































			

		});

	}

}

