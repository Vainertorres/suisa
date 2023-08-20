function registrarPaciente(){
	$.ajax({
		data:$('#formpaciente').serialize(),
		url:$('#formpaciente').attr('action'),
		type:$('#formpaciente').attr('method'),
		success: function(response){
			console.log(response);
		},
		error: function(error){
			console.log(error)

		}
	});
}