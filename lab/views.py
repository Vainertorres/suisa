from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from cnf.views import Sin_privilegio
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from twilio.rest import Client
import urllib3
#import urllib.request
#import urllib.parse
import http.client
import json

from .models import RepLaboratorio, TipoExamen
from cnf.models import TomadorDecision, Paciente, Muestra
from .forms import RepLaboratorioForm

# Create your views here.
def enviarsmsC3(numtel, msg):
	url = 'https://sistemasmasivos.com/c3colombia/api/sendsms/send.php?user=ferneli79@hotmail.com&password=NFNtfONtJd&GSM={}&SMSText={}'.format(numtel, msg)
	return url


def enviarsms( mensaje): #Ya no esta en uso
	tomadesicion = TomadorDecision.objects.all()
	for td in tomadesicion:
		celular = '+57'+td.telefono
		# Your Account SID from twilio.com/console
		account_sid = "AC53597404721eef033c1852de7a5d1e3f"
		# Your Auth Token from twilio.com/console
		auth_token  = "881ec9a6487699305143a74ace390ae1"

		client = Client(account_sid, auth_token)

		message = client.messages.create(
			to=celular, 
	    	from_="+19132858389",
	    	body=mensaje)
		print(message.sid)

# def alertaLaboratorioEmail(request):
	

class RepLaboratorioList(Sin_privilegio, generic.ListView):
	permission_required="lab.view_replaboratorio"
	model = RepLaboratorio
	template_name='lab/replaboratorios_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'


class RepLaboratorioCreate(Sin_privilegio, generic.CreateView):
	permission_required="lab.add_replaboratorio"
	model = RepLaboratorio
	template_name = 'lab/replaboratorios_form.html'
	context_object_name = 'obj'
	form_class = RepLaboratorioForm	
	success_url = reverse_lazy('lab:reportelab_list')
	login_url = 'cnf:login'

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)	
		idpaciente = request.POST['paciente']
		idtipoex = request.POST['tipoexamen']
		tipoexamen = TipoExamen.objects.filter(id=idtipoex).first()
		idmuestra = request.POST['muestra']
		muestra = Muestra.objects.filter(id=idmuestra).first()
		td = TomadorDecision.objects.all()
		telefono = ''
		for x in td:
			if telefono=='':
				telefono = x.telefono
			else:
				telefono = telefono+',{}'.format(x.telefono)

		paciente = Paciente.objects.filter(id=idpaciente).first();
		if form.is_valid():
			form.save()
			if request.POST['resultado'] == 'POS':
				mensaje = "¨Paciente: {} - Tel Contacto: {} - Tiene un resultado POSITIVO DE LABORATORIO: {}, \
				Realizado el Día: {} en una muesta de: {}".format(paciente, paciente.telefono, tipoexamen, \
				request.POST['fecharesultado'], muestra)
				print(telefono)
				envio = enviarsmsC3(telefono, mensaje)				
				print(envio)
				http = urllib3.PoolManager()
				r = http.request('GET', envio)
				print(r.status)

		return redirect('lab:reportelab_list')

class RepLaboratorioUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="lab.change_replaboratorio"
	model = RepLaboratorio
	template_name = 'lab/replaboratorios_form.html'
	context_object_name = 'obj'
	form_class = RepLaboratorioForm	
	success_url = reverse_lazy('lab:reportelab_list')
	login_url = 'cnf:login'
