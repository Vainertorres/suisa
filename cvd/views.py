from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
import folium
from folium.plugins import MarkerCluster
import pandas as pd 
from twilio.rest import Client

from bai.models import Diagnosticos
from cnf.models import Paciente, Tipodoc, Regimen, Area, Sexo, Etnia, UmEdad, Ocupacion, \
 	Departamento, Municipio,ClasiFinicial, Upgd, Evento, Eps, Pais, Barrio
from .models import Bac, Fichaiec, Antecedenteviaje, SegFichaIec, Conglomerado, Notif_covid, \
	ImportSivCvdFile, AntecHospitalizacion, FileFichaIec, ContactosIec, SegContacto,\
	DesplazaContacto, SegContacto, NotifPaConglomerado, ContactoAislado, SegContactoAislado, \
	ConfigConglomerado
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from cnf.views import Sin_privilegio
from django.views import generic

from .forms import BacForm, FichaiecForm, AntViajeForm, SegFichaIecForm, ConglomeradoForm, \
		ImportFileCvdForm, NotifCovidForm, AntHospitalizacionForm, FileIecForm, ContactosForm,\
		DesplazaContactoForm, SeguimientoContactoForm, NotifPaConglomeradoForm, ContactoAisladoForm, \
		SegContactoAisladoForm, ConfigConglomeradoForm

from cnf.views import PacienteForm

from datetime import datetime
from django.contrib import messages
from datetime import date
from datetime import datetime
import webbrowser
# Create your views here.

def createNewPac(request):
	tipodocid = request.GET.get('idtipodoc')
	ident = request.GET.get('ident')
	nombre1 = request.GET.get('nombre1')
	nombre2 = request.GET.get('nombre2')
	apellido1 = request.GET.get('apellido1')
	apellido2 = request.GET.get('apellido2')
	depto = request.GET.get('iddpto')
	idmpio = request.GET.get('idmunicipio')
	idbarrio =request.GET.get('idbarrio')
	direccion =request.GET.get('direccion')
	telefono = request.GET.get('telefono')
	email = request.GET.get('correoelectronico')
	area = request.GET.get('area')
	fn =request.GET.get('fechanac')
	sex = request.GET.get('idsexo')
	idetnia = request.GET.get('idetnia')
	idregimen = request.GET.get('idregimen')
	ideps = request.GET.get('ideps')

	ultimopaciente = Paciente.objects.filter(tipodoc_id=tipodocid).filter(identificacion=ident).first()

	if ultimopaciente:		
		pass
	else:
		pac = Paciente()
		pac.tipodoc_id = tipodocid
		pac.identificacion = ident;
		pac.nombre1 = nombre1;
		pac.nombre2 = nombre2;
		pac.apellido1 = apellido1;
		pac.apellido2 = apellido2;
		pac.departamento_id = depto
		pac.municipio_id = idmpio
		pac.barrio_id = idbarrio
		pac.direccion = direccion
		pac.telefono = telefono
		pac.correoelectronico = email
		pac.area_id = area
		print("fecha Nac {}".format(fn))
		pac.fechaNac = datetime.strptime(fn, '%d/%m/%Y') 
		pac.sexo_id = sex
		pac.etnia_id = idetnia
		pac.regimen_id = idregimen
		pac.eps_id = ideps
		pac.save()
		ultimopaciente = Paciente.objects.filter(tipodoc_id=tipodocid).filter(identificacion=ident).first()

	pacientes = Paciente.objects.filter(estado=True)
	return render(request, 'cvd/paciente_dropdown_list_options.html', {'pacientes': pacientes, 'ultpac':ultimopaciente})

class PacienteCreate(LoginRequiredMixin, generic.CreateView):
    model = Paciente
    #template_name = 'cvd/paciente_form.html'
    context_object_name = 'obj'
    form_class = PacienteForm
    success_url = reverse_lazy('cnf:paciente_list')
    login_url = 'cnf:login'

    def form_valid(self, form):
        form.instance.uc = self.request.user 
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        context = super(PacienteCreate,self).get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['municipios'] = Municipio.objects.all()             
        return context 

def geolocFichasIEC(request):	
	ficha = Fichaiec.objects.filter(~Q(paciente__lat='SD')).filter(~Q(paciente__lon='SD')).values('estadoiec', 'paciente__identificacion','paciente__lat','paciente__lon')
	
	some_map = folium.Map(location=[3.408825,-76.347660], zoom_start = 15)
	
	for row in ficha:
		lat = row['paciente__lat']
		lon = row['paciente__lon']
		ident = row['paciente__identificacion']
		if row['estadoiec'] == 'FAL':
			some_map.add_child(folium.Marker(location=[lat, lon], popup=ident,icon=folium.Icon(color='black', icon='info-sign')))
		else:
			if row['estadoiec'] == 'CUR':
				some_map.add_child(folium.Marker(location=[lat, lon], popup=ident,icon=folium.Icon(color='green')))
			else:
				some_map.add_child(folium.Marker(location=[lat, lon], popup=ident,icon=folium.Icon(icon='cloud')))
			

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'ficha':ficha, 'hs':html_string}

	return redirect('cvd:iec_list')



class GrafCoomorbCovid(generic.TemplateView):
	template_name='cvd/estcoomorcovid_form.html'

	def cantCoomorbilidad(self, id):
		#anio = datetime.now().year
		data=[]		
		if id==1:
			sint = Fichaiec.objects.filter(asma='SI').count()
		if id==2:
			sint = Fichaiec.objects.filter(epoc='SI').count()			
		if id==3:
			sint = Fichaiec.objects.filter(trastorno_neuro='SI').count()
		if id==4:
			sint = Fichaiec.objects.filter(inmunosupresion='SI').count()
		if id==5:
			sint = Fichaiec.objects.filter(enfrenal='SI').count()
		if id==6:
			sint = Fichaiec.objects.filter(enfcardiaca='SI').count()
		if id==7:
			sint = Fichaiec.objects.filter(enfhematologica='SI').count()
		if id==8:
			sint = Fichaiec.objects.filter(diabetes='SI').count()			
		if id==9:
			sint = Fichaiec.objects.filter(obesidad='SI').count()
		if id==10:
			sint = Fichaiec.objects.filter(enfhepatica='SI').count()
		if id==11:
			sint = Fichaiec.objects.filter(embarazo='SI').count()
		if id==12:
			sint = Fichaiec.objects.filter(tabaquismo='SI').count()
		if id==13:
			sint = Fichaiec.objects.filter(alcoholismo='SI').count()
		if id==14:
			sint = Fichaiec.objects.filter(trastorno_reumatologico='SI').count()			

		data.append(float(sint))		
		return data
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['asma']=self.cantCoomorbilidad(1)
	    context['epoc']=self.cantCoomorbilidad(2)
	    context['trastorno_neuro']=self.cantCoomorbilidad(3)
	    context['inmunosupresion']=self.cantCoomorbilidad(4)
	    context['enfrenal']=self.cantCoomorbilidad(5)
	    context['enfcardiaca']=self.cantCoomorbilidad(6)
	    context['enfhematologica']=self.cantCoomorbilidad(7)
	    context['diabetes']=self.cantCoomorbilidad(8)
	    context['obesidad']=self.cantCoomorbilidad(9)
	    context['enfhepatica']=self.cantCoomorbilidad(10)
	    context['embarazo']=self.cantCoomorbilidad(11)
	    context['tabaquismo']=self.cantCoomorbilidad(12)
	    context['alcoholismo']=self.cantCoomorbilidad(13)
	    context['trastorno_reumatologico']=self.cantCoomorbilidad(14)	    
	    return context


class GrafCovidBarrio(generic.TemplateView):
	template_name='cvd/estcovidbarrio_form.html'

	def reporteCovidBarrio(self):

		barrios = Barrio.objects.all()
		
		diccionario = {}
		data = []
		for x in barrios:
			cantbarrio = Fichaiec.objects.filter(paciente__barrio_id = x.id).count()
			if cantbarrio > 0:
				diccionario = {'name':x.descripcion,'y':cantbarrio}
				data.append(diccionario)

		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['barrio']= self.reporteCovidBarrio()
	    return context



class GrafSintomasCovid(generic.TemplateView):
	template_name='cvd/estsintomascovid_form.html'

	def cantsintoma(self, id):
		#anio = datetime.now().year
		data=[]		
		if id==1:
			sint = Fichaiec.objects.filter(fiebre='SI').count()
		if id==2:
			sint = Fichaiec.objects.filter(tos='SI').count()			
		if id==3:
			sint = Fichaiec.objects.filter(dificultadrespirar='SI').count()
		if id==4:
			sint = Fichaiec.objects.filter(taquipnea='SI').count()
		if id==5:
			sint = Fichaiec.objects.filter(dolorgarganta='SI').count()
		if id==6:
			sint = Fichaiec.objects.filter(nauseas='SI').count()
		if id==7:
			sint = Fichaiec.objects.filter(dolor_torax='SI').count()
		if id==8:
			sint = Fichaiec.objects.filter(mialgia='SI').count()			
		if id==9:
			sint = Fichaiec.objects.filter(diarrea='SI').count()
		if id==10:
			sint = Fichaiec.objects.filter(dolor_abdominal='SI').count()
		if id==11:
			sint = Fichaiec.objects.filter(dolor_cabeza='SI').count()
		if id==12:
			sint = Fichaiec.objects.filter(malestar_general='SI').count()
		if id==13:
			sint = Fichaiec.objects.filter(otro='SI').count()
		if id==14:
			sint = Fichaiec.objects.filter(vomito='SI').count()			

		data.append(float(sint))		
		return data
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['fiebre']=self.cantsintoma(1)
	    context['tos']=self.cantsintoma(2)
	    context['dificultadrespirar']=self.cantsintoma(3)
	    context['taquipnea']=self.cantsintoma(4)
	    context['dolorgarganta']=self.cantsintoma(5)
	    context['nauseas']=self.cantsintoma(6)
	    context['dolor_torax']=self.cantsintoma(7)
	    context['mialgia']=self.cantsintoma(8)
	    context['diarrea']=self.cantsintoma(9)
	    context['dolor_abdominal']=self.cantsintoma(10)
	    context['dolor_cabeza']=self.cantsintoma(11)
	    context['malestar_general']=self.cantsintoma(12)
	    context['otro']=self.cantsintoma(13)
	    context['vomito']=self.cantsintoma(14)	    
	    return context

def enviarsms(celular, mensaje):
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


class ConfigConglomeradoList(Sin_privilegio, generic.ListView):
	permission_required="cvd.view_configconglomerado"
	model = ConfigConglomerado
	template_name='cvd/configconglomerado_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'

class ConfigConglomeradoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_configconglomerado"
	model = ConfigConglomerado
	template_name = 'cvd/configconglomerado_form.html'
	context_object_name = 'obj'
	form_class = ConfigConglomeradoForm	
	success_url = reverse_lazy('cvd:config_conglomerado_list')
	login_url = 'cnf:login'

class ConfigConglomeradoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_configconglomerado"
	model = ConfigConglomerado
	template_name = 'cvd/configconglomerado_form.html'
	context_object_name = 'obj'
	form_class = ConfigConglomeradoForm	
	success_url = reverse_lazy('cvd:config_conglomerado_list')
	login_url = 'cnf:login'


def enviarSms(request):
	usuario = "ferneli79@hotmail.com"
	password = "NFNtfONtJd"
	celdestino = "3122313729"
	textomsg = "Prueba desde Suisa"
	url="https://sistemasmasivos.com/c3colombia/api/sendsms/send.php?user={}&password={}&GSM=57{}&SMSText={}".format(usuario, password, celdestino, textomsg)
	return HttpResponse(url)



class SegContactoAisladoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_segcontactoaislado"
	model = SegContactoAislado
	template_name = 'cvd/segcontactocasosempresa_form.html'
	context_object_name = 'obj'
	form_class = SegContactoAisladoForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(SegContactoAisladoCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('id') # El mismo nombre que en tu URL
		contactoaislado = ContactoAislado.objects.get(pk=pk)
		context['contacto'] = contactoaislado
		context['idcontacto'] = pk				
		return context

	def get_success_url(self):
		contactoaislado=self.request.POST['contactoaislado']
		return reverse_lazy('cvd:contactopacnotif_edit', kwargs={'pk':contactoaislado})


class SegContactoAisladoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_segcontactoaislado"
	model = SegContactoAislado
	template_name = 'cvd/segcontactocasosempresa_form.html'
	context_object_name = 'obj'
	form_class = SegContactoAisladoForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(SegContactoAisladoUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		seg = SegContactoAislado.objects.get(pk=pk)
		contactoaislado = ContactoAislado.objects.get(pk=seg.contactoaislado_id)
		context['contacto'] = contactoaislado
		context['idcontacto'] = contactoaislado.pk				
		return context

	def get_success_url(self):
		contactoaislado=self.request.POST['contactoaislado']
		return reverse_lazy('cvd:contactopacnotif_edit', kwargs={'pk':contactoaislado})



class ContactoAisladoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_contactoaislado"
	model = ContactoAislado
	template_name = 'cvd/fichacontactocasosempresa_form.html'
	context_object_name = 'obj'
	form_class = ContactoAisladoForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(ContactoAisladoCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('id') # El mismo nombre que en tu URL
		notifconglomerado = NotifPaConglomerado.objects.get(pk=pk)
		context['notifcong'] = notifconglomerado
		context['idnotifcong'] = pk				
		return context

	def get_success_url(self):
		notifpaconglomerado=self.request.POST['notifPaConglomerado']
		return reverse_lazy('cvd:paconglomerado_edit', kwargs={'pk':notifpaconglomerado})


class ContactoAisladoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_contactoaislado"
	model = ContactoAislado
	template_name = 'cvd/fichacontactocasosempresa_form.html'
	context_object_name = 'obj'
	form_class = ContactoAisladoForm	
	login_url = 'cnf:login'

	def form_valid(self, form):		
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(ContactoAisladoUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		contacto = ContactoAislado.objects.get(pk=pk)
		notifconglomerado = NotifPaConglomerado.objects.get(pk=contacto.notifPaConglomerado_id)
		seg = SegContactoAislado.objects.filter(contactoaislado_id = contacto.pk)
		context['notifcong'] = notifconglomerado
		context['idnotifcong'] = notifconglomerado.pk				
		context['seguimiento'] = seg			
		return context

	def get_success_url(self):
		notifpaconglomerado=self.request.POST['notifPaConglomerado']
		return reverse_lazy('cvd:paconglomerado_edit', kwargs={'pk':notifpaconglomerado})


class NotifPaConglomeradoList(Sin_privilegio, generic.ListView):
	permission_required="cvd.view_notifpaconglomerado"
	model = NotifPaConglomerado
	template_name='cvd/ficharepcasosempresa_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'



class NotifPaConglomeradoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_notifpaconglomerado"
	model = NotifPaConglomerado
	template_name = 'cvd/ficharepcasosempresa_form.html'
	context_object_name = 'obj'
	form_class = NotifPaConglomeradoForm	
	success_url = 'cvd:paconglomerado_list'
	login_url = 'cnf:login'


class NotifPaConglomeradoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_notifpaconglomerado"
	model = NotifPaConglomerado
	template_name = 'cvd/ficharepcasosempresa_form.html'
	context_object_name = 'obj'
	form_class = NotifPaConglomeradoForm	
	login_url = 'cnf:login'

	def form_valid(self, form):		
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(NotifPaConglomeradoUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		contacto = ContactoAislado.objects.filter(notifPaConglomerado=pk)
		context['contacto'] = contacto
		context['idnotif'] = pk				
		return context

	def get_success_url(self):		
		return reverse_lazy('cvd:paconglomerado_list')



def inactivarNotifPaconglemerado(request, id):
    notif = NotifPaConglomerado.objects.filter(pk=id).first()
    if request.method == 'POST':
        if notif:
            notif.estado = not notif.estado
            notif.save()
            return HttpResponse('OK')
        else:
            return HttpResponse('FAIL')
    return HttpResponse('FAIL')

class GrafCovidSemEpi(generic.TemplateView):
	template_name='cvd/estcvdsemepidemiologica.html'

	def ingresosCovid(self, id):
		anio = datetime.now().year
		data=[]		
		for x in range(1,52):			
			covid = Notif_covid.objects.filter(anio=anio, semana=x, evento__codigo=id).count()
			data.append(float(covid))		
		return data
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['sincovid']=self.ingresosCovid(346)
	    context['iragrave']=self.ingresosCovid(348)

	    #context['dengue_grave']=self.ingresoDengueMes(220)
	    #context['motalidad_dengue']=self.ingresoDengueMes(580)
	    return context

class SeguimientoContactoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_segcontacto"
	model = SegContacto
	template_name = 'cvd/seguimientocontacto_form.html'
	context_object_name = 'obj'
	form_class = SeguimientoContactoForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(SeguimientoContactoCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('id') # El mismo nombre que en tu URL
		contactoiec = ContactosIec.objects.get(pk=pk)
		context['contactoiec'] = contactoiec
		context['idcontacto'] = pk				
		return context

	def get_success_url(self):
		contactosiec=self.request.POST['contactosiec']
		return reverse_lazy('cvd:contacto_detalle', kwargs={'id':contactosiec})


class SeguimientoContactoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_segcontacto"
	model = SegContacto
	template_name = 'cvd/seguimientocontacto_form.html'
	context_object_name = 'obj'
	form_class = SeguimientoContactoForm	
	login_url = 'cnf:login'

	def form_valid(self, form):		
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(SeguimientoContactoUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		contactoiec = ContactosIec.objects.get(pk=pk)
		context['contactoiec'] = contactoiec
		context['idcontacto'] = pk				
		return context

	def get_success_url(self):
		contactosiec=self.request.POST['contactosiec']
		return reverse_lazy('cvd:contacto_detalle', kwargs={'id':contactosiec})

def contactoIecDetail(request, id):
	template_name= 'cvd/segcontactosview_form.html'
	contacto = ContactosIec.objects.filter(pk=id).first()
	segcon = SegContacto.objects.filter(contactosiec_id =contacto.id)
	desplaza = DesplazaContacto.objects.filter(contactosiec_id =contacto.id)

	contexto = {'segcon':segcon,'desplaza':desplaza,'obj':contacto}
	return render(request, template_name, contexto)

class DesplazaContactoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_desplazacontacto"
	model = DesplazaContacto
	template_name = 'cvd/desplazacontacto_form.html'
	context_object_name = 'obj'
	form_class = DesplazaContactoForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(DesplazaContactoCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('id') # El mismo nombre que en tu URL
		contactoiec = ContactosIec.objects.get(pk=pk)
		context['contactoiec'] = contactoiec
		context['idcontacto'] = pk				
		return context

	def get_success_url(self):
		contactosiec=self.request.POST['contactosiec']
		return reverse_lazy('cvd:contacto_detalle', kwargs={'id':contactosiec})

class DesplazaContactoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_desplazacontacto"
	model = DesplazaContacto
	template_name = 'cvd/desplazacontacto_form.html'
	context_object_name = 'obj'
	form_class = DesplazaContactoForm	
	login_url = 'cnf:login'

	def form_valid(self, form):		
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(DesplazaContactoUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		contactoiec = ContactosIec.objects.get(pk=pk)
		context['contactoiec'] = contactoiec
		context['idcontacto'] = pk				
		return context

	def get_success_url(self):
		contactosiec=self.request.POST['contactosiec']
		return reverse_lazy('cvd:contacto_detalle', kwargs={'id':contactosiec})


class ContactoIecCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_contactosiec"
	model = ContactosIec
	template_name = 'cvd/contactos_form.html'
	context_object_name = 'obj'
	form_class = ContactosForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(ContactoIecCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idficha') # El mismo nombre que en tu URL
		ficha = Fichaiec.objects.get(pk=pk)
		context['fichaiec'] = ficha
		context['idficha'] = pk				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})


class ContactoIecUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_contactosiec"
	model = ContactosIec
	template_name = 'cvd/contactos_form.html'
	context_object_name = 'obj'
	form_class = ContactosForm	
	login_url = 'cnf:login'

	def form_valid(self, form):		
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(ContactoIecUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		contactosiec =ContactosIec.objects.get(pk=pk) 
		ficha = Fichaiec.objects.get(pk=contactosiec.fichaiec.id)
		context['fichaiec'] = ficha
		context['idficha'] = ficha.id				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})

class ContactoIecList(Sin_privilegio, generic.ListView):
    permission_required="cvd.view_contactosiec"
    model = ContactosIec
    template_name='cvd/contactoiec_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class FileIecList(Sin_privilegio, generic.ListView):
    permission_required="cvd.view_filefichaiec"
    model = FileFichaIec
    template_name='cvd/filefichaiec_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'


class FileIecCreate(Sin_privilegio, generic.CreateView):
	#form = FileIecForm(request.POST or None, request.FILES or None)
	permission_required="cvd.add_filefichaiec"
	model = FileFichaIec
	template_name = 'cvd/filefichaiec_form.html'
	context_object_name = 'obj'
	form_class = FileIecForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(FileIecCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idficha') # El mismo nombre que en tu URL
		ficha = Fichaiec.objects.get(pk=pk)
		context['fichaiec'] = ficha
		context['idficha'] = pk				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})

class FileIecUpdate(Sin_privilegio, generic.UpdateView):
	#form = FileIecForm(request.POST or None, request.FILES or None)
	permission_required="cvd.change_filefichaiec"
	model = FileFichaIec
	template_name = 'cvd/filefichaiec_form.html'
	context_object_name = 'obj'
	form_class = FileIecForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(FileIecUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		filefichaiec =FileFichaIec.objects.get(pk=pk) 
		ficha = Fichaiec.objects.get(pk=filefichaiec.fichaiec.id)
		context['fichaiec'] = ficha
		context['idficha'] = ficha.id				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})


class AntecHospitalizacionCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_antechospitalizacion"
	model = AntecHospitalizacion
	template_name = 'cvd/antecedente_hospitalizacion.html'
	context_object_name = 'obj'
	form_class = AntHospitalizacionForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(AntecHospitalizacionCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idficha') # El mismo nombre que en tu URL
		ficha = Fichaiec.objects.get(pk=pk)
		context['fichaiec'] = ficha
		context['idficha'] = pk				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})

class AntecHospitalizacionUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_antechospitalizacion"
	model = AntecHospitalizacion
	template_name = 'cvd/antecedente_hospitalizacion.html'
	context_object_name = 'obj'
	form_class = AntHospitalizacionForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(AntecHospitalizacionUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		anthosp =AntecHospitalizacion.objects.get(pk=pk) 
		ficha = Fichaiec.objects.get(pk=anthosp.fichaiec.id)
		context['fichaiec'] = ficha
		context['idficha'] = ficha.id				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})

def anexos_fichaIec(request, id):
	template_name= 'cvd/fichaiecviewform.html'
	fichaiec = Fichaiec.objects.filter(pk=id).first()
	viaje = Antecedenteviaje.objects.filter(fichaiec=fichaiec)
	anthos = AntecHospitalizacion.objects.filter(fichaiec=fichaiec) 
	fileiec = FileFichaIec.objects.filter(fichaiec=fichaiec) 
	contacto = ContactosIec.objects.filter(fichaiec=fichaiec)
	contexto = {'ficha':fichaiec, 'obj':viaje, 'anthos':anthos, 'fileiec':fileiec, 'contacto':contacto}
	return render(request, template_name, contexto)


class AntecedenteViajeCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_fichaiec"
	model = Antecedenteviaje
	template_name = 'cvd/antecedente_viaje.html'
	context_object_name = 'obj'
	form_class = AntViajeForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(AntecedenteViajeCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idficha') # El mismo nombre que en tu URL
		ficha = Fichaiec.objects.get(pk=pk)
		context['fichaiec'] = ficha
		context['idficha'] = pk				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})

class AntecedenteViajeUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_fichaiec"
	model = Antecedenteviaje
	template_name = 'cvd/antecedente_viaje.html'
	context_object_name = 'obj'
	form_class = AntViajeForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(AntecedenteViajeUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		antviaje =Antecedenteviaje.objects.get(pk=pk) 
		ficha = Fichaiec.objects.get(pk=antviaje.fichaiec.id)
		context['fichaiec'] = ficha
		context['idficha'] = ficha.id				
		return context

	def get_success_url(self):
		idficha=self.request.POST['fichaiec']
		return reverse_lazy('cvd:ver_fichaiec', kwargs={'id':idficha})

def seguimientoNotifCovid(request, id):    
	template_name= 'cvd/notifi_covid.html'
	obj = Notif_covid.objects.filter(pk=id).first()
	contexto = {'form':obj}
	form_class = NotifCovidForm
	return render(request, template_name, contexto)
	
def notifCovidList(request):
    modelo = Notif_covid.objects.all().order_by('-fec_not')[:500]
    template_name='cvd/notif_covid_list.html'
    contexto ={"obj":modelo}
    return render(request, template_name, contexto)

def geolocConglomerado(request):	
	conglomerado = Conglomerado.objects.filter(~Q(lat='SD')).filter(~Q(lon='SD'))
	
	some_map = folium.Map(location=[3.408825,-76.347660], zoom_start = 15)
	
	for row in conglomerado:
		some_map.add_child(folium.Marker(location=[row.lat, row.lon], popup=row.descripcion))

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'conglomerado':conglomerado, 'hs':html_string}

	return redirect('cvd:conglomerado_list')

class ConglomeradoList(Sin_privilegio, generic.ListView):
    permission_required="cvd.view_conglomerado"
    model = Conglomerado
    template_name='cvd/conglomerado_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class ConglomeradoCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_conglomerado"
	model = Conglomerado
	template_name = 'cvd/conglomerado_form.html'
	context_object_name = 'obj'
	form_class = ConglomeradoForm
	success_url = reverse_lazy('cvd:conglomerado_list')
	login_url = 'cnf:login'    

class ConglomeradoEdit(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_conglomerado"
	model = Conglomerado
	template_name = 'cvd/conglomerado_form.html'
	context_object_name = 'obj'
	form_class = ConglomeradoForm
	success_url = reverse_lazy('cvd:conglomerado_list')
	login_url = 'cnf:login' 

class BacList(Sin_privilegio, generic.ListView):
    permission_required="cvd.view_bac"
    model = Bac
    template_name='cvd/bac_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'


class BacCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_bac"
	model = Bac
	template_name = 'cvd/bac_form.html'
	context_object_name = 'obj'
	form_class = BacForm
	success_url = reverse_lazy('cvd:bac_list')
	login_url = 'cnf:login'

	"""def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)  """

class BacEdit(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.add_bac"
	model = Bac
	template_name = 'cvd/bac_form.html'
	context_object_name = 'obj'
	form_class = BacForm
	success_url = reverse_lazy('cvd:bac_list')
	login_url = 'cnf:login'


class FichaIecList(Sin_privilegio, generic.ListView):
    permission_required="cvd.view_fichaiec"
    model = Fichaiec
    template_name='cvd/fichaiec_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'


class FichaIecCreate(Sin_privilegio, generic.CreateView):
	permission_required="cvd.new_fichaiec"
	model = Fichaiec
	template_name="cvd/fichaiecform.html"
	form_class=FichaiecForm
	context_object_name = 'obj'
	success_url = reverse_lazy('cvd:iec_list')
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(FichaIecCreate,self).get_context_data(**kwargs)
		context['departamentos'] = Departamento.objects.all()
		context['municipios'] = Municipio.objects.all()				
		context['tipodocs'] = Tipodoc.objects.filter(estado=True)				
		context['regimenes'] = Regimen.objects.filter(estado=True)				
		context['epss'] = Eps.objects.filter(estado=True)	
		context['barrios'] = Barrio.objects.filter(estado=True)	
		context['etnias'] = Etnia.objects.filter(estado=True)	
		context['areas'] = Area.objects.filter(estado=True)			
		context['sexos'] = Sexo.objects.filter(estado=True)	
		return context

class FichaIecEdit(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_fichaiec"
	model = Fichaiec
	template_name = 'cvd/fichaiecform.html'
	context_object_name = 'obj'
	form_class = FichaiecForm
	success_url = reverse_lazy('cvd:iec_list')
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		pk = self.kwargs.get('pk')
		context = super(FichaIecEdit,self).get_context_data(**kwargs)
		context['departamentos'] = Departamento.objects.all()
		context['municipios'] = Municipio.objects.all()		
		context['tipodocs'] = Tipodoc.objects.filter(estado=True)				
		context['regimenes'] = Regimen.objects.filter(estado=True)				
		context['epss'] = Eps.objects.filter(estado=True)	
		context['barrios'] = Barrio.objects.filter(estado=True)	
		context['etnias'] = Etnia.objects.filter(estado=True)	
		context['areas'] = Area.objects.filter(estado=True)					
		context['sexos'] = Sexo.objects.filter(estado=True)	
		context['obj'] = Fichaiec.objects.filter(pk=pk).first()
		return context

def tareasSegIec(request):
	template='cvd/tareas_segiec_list.html'
	model = SegFichaIec.objects.all()
	context_object_name = 'obj'
	contexto={
		'obj':model
	}
	return render(request,template,contexto)


class SeguimientoIecList(Sin_privilegio, generic.ListView):
    permission_required="cvd.view_segfichaiec"
    model = SegFichaIec
    template_name='cvd/seguimiento_fichaiec_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class SeguimientoIecNew(Sin_privilegio, generic.CreateView):
	permission_required="cvd.add_segfichaiec"
	model = SegFichaIec
	template_name = 'cvd/segfichaiec_form.html'
	context_object_name = 'obj'
	form_class = SegFichaIecForm
	success_url = reverse_lazy('cvd:iec_seguimiento_list')
	login_url = 'cnf:login'

class SeguimientoIecedit(Sin_privilegio, generic.UpdateView):
	permission_required="cvd.change_segfichaiec"
	model = SegFichaIec
	template_name = 'cvd/segfichaiec_form.html'
	context_object_name = 'obj'
	form_class = SegFichaIecForm
	success_url = reverse_lazy('cvd:iec_seguimiento_list')
	login_url = 'cnf:login'

def importarCovid19(request):
	form = ImportFileCvdForm(request.POST or None, request.FILES or None)
	template='cvd/importcovid.html'
	contexto = {'form':form} 	
	linea=[]
	
	if request.method == 'POST':
		sem = int(request.POST['semepidemiologica'])

	if form.is_valid():
		form.save()
		form = ImportFileCvdForm()
		obj = ImportSivCvdFile.objects.get(activated=False)
		with open(obj.file_name.path, 'r') as url:
			df = pd.read_excel(obj.file_name, encoding='latin1')
			#df = pd.read_excel(url)

			dfnew = df.fillna(value=0)
			
			
			#print(xls.sheet_names) nombre de las pestañas
			#df = xls.parse('Hoja1')			
			for i, row in dfnew.iterrows():
				cod_eve = row['cod_eve']
				tipodoc = row['tip_ide_']
				ident = row['num_ide_']
				nom1 = row['pri_nom_']
				nom2 =  row['seg_nom_']				
				apel1 = row['pri_ape_']
				apel2 = row['seg_ape_']
				direcc = row['dir_res_']
				tel = row['telefono_']
				fecha_nac = row['fecha_nto_']
				reg = row['tip_ss_']
				epsvar = row['cod_ase_']
				etnia = row['per_etn_']
				area = row['area_']
				sexo = row['sexo_']
				gp_gestan =  int(row['gp_gestan'])

							
				td = Tipodoc.objects.get(codigo=tipodoc)
				if reg != 0:
					regimen = Regimen.objects.filter(codigo=reg).first()				
				ar = Area.objects.get(codigo=area)
				sex = Sexo.objects.get(codigo=sexo)
				et = Etnia.objects.get(pk=etnia)
				if epsvar != '0':
					eapb = Eps.objects.filter(codigo=epsvar).first()

				linea.append([cod_eve, td.descripcion, ident, nom1, nom2, apel1, apel2, direcc, tel,fecha_nac, gp_gestan])
			
				pac = Paciente.objects.filter(tipodoc=td).filter(identificacion=ident).first()
				
				if pac:
					pac.nombre1 = nom1 
					if nom2 != 0:
						pac.nombre2 = nom2 					
					pac.apellido1 = apel1
					if apel2 != 0:
						pac.apellido2 = apel2
					pac.save()
				else:
					pac = Paciente()
					pac.tipodoc_id = td.id
					pac.identificacion = ident
					pac.nombre1 = nom1 
					pac.nombre2 = nom2 					
					pac.apellido1 = apel1
					pac.apellido2 = apel2
					pac.direccion = direcc
					pac.telefono = tel
					pac.fechaNac = fecha_nac				
					pac.uc = request.user
					if et:
						pac.etnia = et
					if regimen:
						pac.regimen = regimen
					if eapb:
						pac.eps = eapb
					if ar:
						pac.area = ar
					if sex:	
						pac.sexo = sex
					pac.save()

							
				anio = row['año']
				fec_not = row['fec_not']
				sem = row['semana']
				cod_pre = row['cod_pre']
				cod_sub = row['cod_sub']
				edad = row['edad_']

				umed = row['uni_med_']
				umedad = UmEdad.objects.filter(codigo=umed).first()

				ocupa = row['ocupacion_']
				ocupacion = Ocupacion.objects.filter(codigo=ocupa).first()
			
				estrato = int(row['estrato_'])
				gp_discapa = int(row['gp_discapa'])
				gp_desplaz = int(row['gp_desplaz'])
				gp_migrant = int(row['gp_migrant'])
				gp_carcela = int(row['gp_carcela'])
				gp_gestan =  int(row['gp_gestan'])
				sem_ges = int(row['sem_ges_'])

				gp_indigen = int(row['gp_indigen'])
				gp_pobicbf = int(row['gp_pobicbf'])
				gp_mad_com = int(row['gp_mad_com'])
				gp_desmovi = int(row['gp_desmovi'])
				gp_psiquia = int(row['gp_psiquia'])
				gp_vic_vio = int(row['gp_vic_vio'])
				gp_otros = int(row['gp_otros'])
				departamentor = row['ndep_resi']
				dptor = Departamento.objects.filter(codigo=departamentor).first()
				municipior = row['nmun_resi']
				mpior = Municipio.objects.filter(codigo=municipior).first()
				fec_con = row['fec_con_']
				ini_sin = row['ini_sin_']
				clasIni = int(row['tip_cas_'])
				clasiFinicial = ClasiFinicial.objects.filter(pk=clasIni).first()
				pac_hos = row['pac_hos_']
				fec_hos = row['fec_hos_']				
				nit_upgd = row['nit_upgd']
				upgd = Upgd.objects.filter(nitcc=nit_upgd).first()
				
				cefalea = int(row['cefalea'])
				con_fin = int(row['con_fin_'])
				fed_def =  row['fec_def_']
				cer_def = row['cer_def_']
				if row['cbmte_'] == 0.0:
					cbmte = '0'
				else:
					cbmte = row['cbmte_']
				dx = Diagnosticos.objects.filter(codigo=cbmte).first()

				if dx:
					dxmuerte = dx
				telefono = row['telefono_']				
				trab_salud = int(row['trab_salud'])
				deter_clin = int(row['deter_clin'])
				asoc_brote = int(row['asoc_brote'])
				viaje = int(row['viajó'])
				municipioviajo = row['nal_muni'] 
				codpais_pr = int(row['codpais_pr'])
				codpais = Pais.objects.filter(codigo=codpais_pr).first()
				con_con = int(row['con_con'])
				con_est = int(row['con_est']) #contacto estrecho
				tos = int(row['tos'])
				fiebre = int(row['fiebre'])
				odinofagia	= int(row['odinofagia'])
				dif_res	= int(row['dif_res'])
				adinamia = int(row['adinamia'])
				vac_ei = int(row['vac_ei']) #VACUNCION INFLUENZA
				dos_ei = int(row['dos_ei'])
				asma = int(row['asma'])
				epoc = int(row['epoc'])
				diabetes = int(row['diabetes'])
				vih = int(row['vih'])
				enf_card = int(row['enf_card'])
				cancer = int(row['cancer'])
				desnutricion = int(row['desnutricion'])
				obesidad = int(row['obesidad'])
				ins_renal = int(row['ins_renal'])
				otr_medinm =int(row['otr_medinm'])
				fumador = int(row['fumador'])
				tuberculos = int(row['tuberculos'])
				otros_dc = int(row['otros_dc'])
				cual_ot_dc = row['cual_ot_dc']
				hallaz_rad = int(row['hallaz_rad'])
				uso_antib = int(row['uso_antib'])
				uso_antiv = int(row['uso_antiv'])
				fec_antiv = row['fec_antiv']
				serv_hosp = int(row['serv_hosp'])
				fec_inguci = row['fec_inguci']
				der_ple = int(row['der_ple']) #derrame pleural
				der_per = int(row['der_per'])
				miocarditi = int(row['miocarditi'])
				septicemia = int(row['septicemia'])
				falla_resp = int(row['falla_resp'])
				otros_sint = int(row['otros']) #Otros sintomas
				dol_gar = int(row['dol_gar'])
				rinorrea = int(row['rinorrea'])
				conjuntivi = int(row['conjuntivi'])
				diarrea = int(row['diarrea'])
				rx_torax = int(row['rx_torax'])
				fec_tom_ra = row['fec_tom_ra']
				fec_atib =  row['fec_atib']
				otros_cual = row['otros_cual']
				if row['dx_ini']==0.0:
					dx_ini = '0'
				else:
					dx_ini = row['dx_ini']

				if row['dx_egr']==0.0:
					dx_egr = '0'
				else:
					dx_egr = row['dx_egr']

				semana_ges = int(row['semana_ges'])

				even = Evento.objects.filter(codigo=cod_eve).first()

				covid = Notif_covid.objects.filter(paciente=pac).filter(semana=sem).filter(evento=even).first()
				if covid:
					pass
				else:
					covid = Notif_covid()					
					covid.evento = even					
					covid.paciente = pac		
					covid.fec_not = fec_not	
					covid.semana = sem	
					covid.anio = anio
					covid.cod_pre = cod_pre	
					covid.cod_sub = cod_sub
					covid.edad = edad
					if umedad:
						covid.umedad = umedad
					if ocupacion:
						covid.ocupacion = ocupacion
					if regimen:
						covid.regimen = regimen
					if eapb:
						covid.eps = eapb
					covid.estrato = estrato
					covid.gp_discapa = int(gp_discapa)
					covid.gp_desplaz = int(gp_desplaz)
					covid.gp_migrant = int(gp_migrant)
					covid.gp_carcela = int(gp_carcela)
					covid.gp_gestan = int(gp_gestan)
					if sem_ges == '0':
						covid.sem_ges = 0
					else:
						covid.sem_ges = int(sem_ges)

					covid.gp_indigen = int(gp_indigen)
					covid.gp_pobicbf = int(gp_pobicbf)
					covid.gp_mad_com= int(gp_mad_com)
					covid.gp_desmovi = int(gp_desmovi)
					covid.gp_psiquia = int(gp_psiquia)
					covid.gp_vic_vio = int(gp_vic_vio)
					covid.gp_otros = int(gp_otros)
					if dptor:
						covid.Departamentor = dptor
					if mpior:
						covid.municipior = mpior
					
					if clasiFinicial:
						covid.clasiFinicial = clasiFinicial

					covid.pac_hos = int(pac_hos)
					if fec_hos =='  -   -':
						pass
					else:
						covid.fec_hos = fec_hos
					covid.con_fin = con_fin

					if ini_sin =='  -   -':
						pass
					else:
						covid.ini_sin = ini_sin

					if upgd:
						covid.upgd = upgd

					covid.con_fin = con_fin

					if fed_def =='  -   -':
						pass
					else:
						covid.fed_def = fed_def

					if cer_def != 0.0:						
						covid.cer_def = cer_def

					dxmuerte = Diagnosticos.objects.filter(codigo=cbmte).first()

					if dxmuerte:
						dxmuerte = dxmuerte

					covid.trab_salud = int(trab_salud)
					covid.deter_clin = deter_clin
					covid.asoc_brote = asoc_brote
					if not viaje == 0:
						covid.viaje = viaje
					covid.municipioviajo = municipioviajo 
					if codpais:
						covid.codpais_pr = codpais

					covid.con_con = con_con
					covid.con_est = con_est #contacto estrecho					
					covid.tos = int(tos)
					covid.fiebre = int(fiebre)
					covid.odinofagia = odinofagia
					covid.dif_res = int(dif_res)
					covid.adinamia = int(adinamia)
					covid.vac_ei = int(vac_ei)
					covid.dos_ei = dos_ei
					covid.asma = int(asma)
					covid.epoc = int(epoc)
					covid.diabetes = int(diabetes)
					covid.vih = int(vih)
					covid.enf_card = enf_card
					covid.cancer = cancer
					covid.desnutricion = desnutricion
					covid.obesidad = obesidad
					covid.ins_renal = ins_renal
					covid.otr_medinm = otr_medinm
					covid.fumador = fumador
					covid.tuberculos = tuberculos
					covid.otros_dc = otros_dc
					covid.cual_ot_dc = cual_ot_dc
					covid.hallaz_rad = hallaz_rad
					covid.uso_antib = uso_antib
					covid.uso_antiv = uso_antiv
					if (fec_antiv =='  -   -' or fec_antiv == 0):
						fec_antiv='-1'
					else:
						covid.fec_antiv = fec_antiv	

					covid.serv_hosp = serv_hosp

					if (fec_inguci =='  -   -' or fec_inguci==0):
						fec_inguci = '-1'
					else:
						covid.fec_inguci = fec_inguci					
					covid.der_ple = der_ple #derrame pleural
					covid.der_per = der_per
					covid.miocarditi = miocarditi
					covid.septicemia = septicemia
					covid.falla_resp = falla_resp
					covid.otros_sint = otros_sint #Otros sintomas
					"""pre_car_v1
					vac_sp
					dos_sp
					fud_sp
					fud_ei"""
					covid.dol_gar = int(dol_gar)
					covid.rinorrea = int(rinorrea)
					covid.conjuntivi = int(conjuntivi)
					covid.cefalea = int(cefalea)
					covid.diarrea = int(diarrea)
					covid.rx_torax = int(rx_torax)

					if (fec_tom_ra =='  -   -' or fec_tom_ra==0):
						fec_tom_ra = '-1'
					else:
						covid.fec_tom_ra = fec_tom_ra
							
					if (fec_atib =='  -   -' or fec_atib == 0):
						fec_atib = '-1'
					else:
						covid.fec_atib = fec_atib

					if not otros_cual == 0.0:
						covid.otros_cual = otros_cual
					covid.dx_ini = dx_ini
					covid.dx_egr = dx_egr
					covid.semana_ges = int(semana_ges)
					covid.save() 
				
			contexto.update({'dfc':linea})		

					#-----------------------------"""

		obj.activated = True
		obj.save()
		return redirect('cvd:notif_covid_sivigila_list')

	return render(request,template, contexto)






 