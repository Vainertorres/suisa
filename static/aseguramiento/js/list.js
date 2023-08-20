$(function(){


	$('#tblcont').DataTable({
		responsive: true,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ajax: {
	    url: window.location.pathname,
	    type: 'POST',
	    data: {
	    	'action':'searchdata'
	    }, // parametros
	    dataSrc: ""
	},
	columns: [
	    { "data": "id"},
	    { "data": "identificacion"},
	    { "data": "razonsocial"},
	    { "data": "fechanac"},
	    { "data": "eps__descripcion"},
	    { "data": "fechaafiliacion"},
	    { "data": "estadoactual"},
	    
	],
	columnDefs: [
	    {
	        targets: [-1],
	        class: 'text-center',
	        orderable: false,
	        render: function (data, type, row) {
	            return data;
	        }
	    },
	],
	initComplete: function(settings, json) {

		//alert('Tabla cargada');

	  }

	});

});