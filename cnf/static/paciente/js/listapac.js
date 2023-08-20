$(function(){
	$('tblpaciente').DataTable({
		responsive : true,
		autoWidth: false,
		destroy : true,
		deferRender : true,
		ajax: {
			url : window.location.pathname,
			type: 'POST',
			data: {
				'action':'searchdata'
			},
			dataSrc : ""
		},
		columns:[
			{"data":"tipodoc"}
			{"data":"identificacion"}
			{"data":"nombres"}
			{"data":"apellidos"}
			{"data":"direccion"}
			{"data":"telefono"}
			{"data":"estado"}
			{"data":"estado"}


		],
		columnDefs:[
		{
			targets : [2],
			class : "text-center",
			orderable : true,
			render: function(data, type, row){
				return data;
			}

		},
		{
			targets : [3],
			class : "text-center",
			orderable : true,
			render: function(data, type, row){
				return data;
			}

		},

		],
		initComplete : function(settings, json) {

		}
	});
});