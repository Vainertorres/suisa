$(document).ready(function() {
	
	
	$('#datarediarios').DataTable({		
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
	    	{ "data": "fecha"},
	    	{ "data": "tipodoc"},
	    	{ "data": "identificacion"},
	    	{ "data": "razonsocial"},	    
	    	{ "data": "edad"},
	   		{ "data": "telefono"},
	   		{ "data": "eapb"},	    	
	    	{ "data": "laboratorio"},
	    	{ "data": "dosisaplicada"},
	    	{ "data": "nombreIps"},
	    	{ "data": "nombreIps"},	   
		],
	columnDefs: [
	    {
	        targets: [-1],
	        class: 'text-center',
	        orderable: false,
	        render: function (data, type, row) {
	            //var buttons = '<a href="/pai/rediario/update/' + row.id + '" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
	            var buttons = '<a href="/pai/rediario/print/' + row.id + '" class="btn btn-warning btn-xs btn-flat"><i class="fa-solid fa-print"></i></a> ';
                return buttons;
	        }
	    },
	],
	initComplete: function(settings, json) {

		//alert('Tabla cargada');

	  }

	});

});