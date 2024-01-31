from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum

from folium.plugins import MarkerCluster
from django.views import generic
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from django.conf import settings
from .models import Dengue, Conducta, ClasiFinalDen

from cnf.models import Tipodoc, Paciente, Regimen, Eps, Area, Etnia, Sexo, Evento, SemEpidemiologica, UmEdad, \
Ocupacion, Departamento, Municipio, ClasiFinicial, Upgd
# Create your views here.
from cnf.views import Sin_privilegio
from .forms import ImportFileForm, DengueForm, SegPacDengueForm, FileDengueForm, IecDengueForm, \
	ContactIecDengueForm
from .models import ImportarFile, SegPacDengue, FilePacDengue, IecDengue, ContactoIecDen
import folium
import pandas as pd
import webbrowser

from folium.plugins import HeatMap

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name='base/basedengue.html'
    login_url='cnf:login'


class EstDengueSemEpi(generic.TemplateView):
	template_name = 'den/estadisticadenguesemepidemiologica_form.html'


class GrafDengueSemEpi(generic.TemplateView):
	template_name='den/estdenguesemepidemiologica.html'
	 
	
	def ingresos_dengue(self, id):
		#anio = datetime.now().year
		anio = 2020
		denguemax = Dengue.objects.all().aggregate(Max('semana'))
		rangofin=denguemax['semana__max']
		rangofin+=1
		data=[]		
		for x in range(1, rangofin):	
			if id == 1:
				dengue = Dengue.objects.filter(anio=anio, evento__codigo=210, semana=x).count()
			else:
				if id == 2:
					dengue = Dengue.objects.filter(anio=anio, evento__codigo=220, semana=x).count()
				else:
					dengue = Dengue.objects.filter(anio=anio, evento__codigo=580, semana=x).count()
			data.append(float(dengue))		
		return data

	def rango_fin(self):
		denmax = Dengue.objects.all().aggregate(Max('semana'))
		rangofin=denmax['semana__max']
		return rangofin

	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)		       
	    context['panel']='Panel de Administrador'
	    context['dengue']=self.ingresos_dengue(1)
	    context['denguegrave']=self.ingresos_dengue(2)
	    context['mortaldengue']=self.ingresos_dengue(3)
	    context['rangoini']=1
	    context['rangofin']=self.rango_fin()
	    return context


def geolocDengue210(request):	
	dengue = Dengue.objects.filter(~Q(paciente__lat='SD')).filter(~Q(paciente__lon='SD')).values('paciente__identificacion','paciente__lat','paciente__lon')

	some_map = folium.Map(location=[3.534089,-76.298574], zoom_start = 15)
	
	for row in dengue:
		lat = row['paciente__lat']
		lon = row['paciente__lon']
		ident = row['paciente__identificacion']
		some_map.add_child(folium.Marker(location=[lat, lon], popup=ident))

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'dengue':dengue, 'hs':html_string}

	return redirect('den:dengue_list')

def geolocDengue220(request):	
	dengue = Dengue.objects.filter(~Q(paciente__lat='SD')).filter(~Q(paciente__lon='SD')).filter(evento__codigo=220).values('paciente__identificacion','paciente__lat','paciente__lon')

	some_map = folium.Map(location=[3.534089,-76.298574], zoom_start = 15)
	
	for row in dengue:
		lat = row['paciente__lat']
		lon = row['paciente__lon']
		ident = row['paciente__identificacion']
		some_map.add_child(folium.Marker(location=[lat, lon], popup=ident))

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'dengue':dengue, 'hs':html_string}

	return redirect('den:dengue_grave_list')

def mapaCalarDengueGrave(request):
	dengue = Dengue.objects.filter(~Q(paciente__lat='SD')).filter(~Q(paciente__lon='SD')).filter(evento__codigo=220).values('paciente__identificacion','paciente__lat','paciente__lon')

	m = folium.Map(location=[3.534089,-76.298574], zoom_start = 13)
	data = []
	for row in dengue:
		lat = row['paciente__lat']
		lon = row['paciente__lon']
		dato = (lat,lon)
		data.append(dato)
		

	#HeatMap.add_child(some_map3)
	HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
	
	filepath = 'C:/mapas/mapacalor.html'
	m.save(filepath)
	webbrowser.open('file://' + filepath)
	html_string = m.get_root().render()
	context = {'sm':m, 'dengue':dengue, 'hs':html_string}
	return redirect('den:dengue_grave_list')

class ContactoIecDengueCreate(Sin_privilegio, generic.CreateView):
	permission_required="den.add_contactoiecden"
	model = ContactoIecDen
	template_name = 'den/contactPacDengue_form.html'
	context_object_name = 'obj'
	form_class = ContactIecDengueForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(ContactoIecDengueCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idiecdengue') # El mismo nombre que en tu URL
		iecdengue = IecDengue.objects.get(pk=pk)
		context['iecdengue'] = iecdengue
		context['idiecdengue'] = pk		
		return context

	def get_success_url(self):
		idiecdengue=self.request.POST['iecdengue']
		return reverse_lazy('den:iecdengue_edit', kwargs={'pk':idiecdengue})

class ContactoIecDengueUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="den.change_contactoiecden"
	model = ContactoIecDen
	template_name = 'den/contactPacDengue_form.html'
	context_object_name = 'obj'
	form_class = ContactIecDengueForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(ContactoIecDengueUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		contactiecden = ContactoIecDen.objects.get(pk=pk)
		iecdengue = IecDengue.objects.get(pk=contactiecden.iecdengue_id)
		context['iecdengue'] = iecdengue
		context['idiecdengue'] = iecdengue.id	
		#context['ideps'] = dengue.paciente.eps.id	
		return context

	def get_success_url(self):
		idiecdengue=self.request.POST['iecdengue']
		return reverse_lazy('den:iecdengue_edit', kwargs={'pk':idiecdengue})

class IecDengueCreate(Sin_privilegio, generic.CreateView):
	permission_required="den.add_iecdengue"
	model = IecDengue
	template_name = 'den/iecDengue_form.html'
	context_object_name = 'obj'
	form_class = IecDengueForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(IecDengueCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('iddengue') # El mismo nombre que en tu URL
		dengue = Dengue.objects.get(pk=pk)
		context['dengue'] = dengue
		context['iddengue'] = pk	
		#context['ideps'] = dengue.paciente.eps.id	
		return context

	def get_success_url(self):
		iddengue=self.request.POST['dengue']
		return reverse_lazy('den:dengue_edit', kwargs={'iddengue':iddengue})

class IecDengueUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="den.change_iecdengue"
	model = IecDengue
	template_name = 'den/iecDengue_form.html'
	context_object_name = 'obj'
	form_class = IecDengueForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(IecDengueUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		iecdengue =IecDengue.objects.get(pk=pk) 
		dengue = Dengue.objects.get(pk=iecdengue.dengue.id)
		contact = ContactoIecDen.objects.filter(iecdengue=iecdengue)
		context['dengue'] = dengue
		context['iddengue'] = dengue.id	
		context['contact'] = contact	
		return context

	def get_success_url(self):
		iddengue=self.request.POST['dengue']
		return reverse_lazy('den:dengue_edit', kwargs={'iddengue':iddengue})		


class FileDengueCreate(Sin_privilegio, generic.CreateView):
	permission_required="den.add_filepacdengue"
	model = FilePacDengue
	template_name = 'den/filedengue_form.html'
	context_object_name = 'obj'
	form_class = FileDengueForm	
	login_url = 'cnf:login'


	def get_context_data(self, **kwargs):
		context = super(FileDengueCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('iddengue') # El mismo nombre que en tu URL
		dengue = Dengue.objects.get(pk=pk)
		context['dengue'] = dengue
		context['iddengue'] = pk				
		return context

	def get_success_url(self):
		iddengue=self.request.POST['dengue']
		return reverse_lazy('den:dengue_edit', kwargs={'iddengue':iddengue})

class FileDengueUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="den.change_filepacdengue"
	model = FilePacDengue
	template_name = 'den/filedengue_form.html'
	context_object_name = 'obj'
	form_class = FileDengueForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(FileDengueUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		filedengue =FilePacDengue.objects.get(pk=pk) 
		dengue = Dengue.objects.get(pk=filedengue.dengue.id)
		context['dengue'] = dengue
		context['iddengue'] = dengue.id				
		return context

	def get_success_url(self):
		iddengue=self.request.POST['dengue']
		return reverse_lazy('den:dengue_edit', kwargs={'iddengue':iddengue})		


class GrafDenguemes(generic.TemplateView):
	template_name='den/estdenguemes.html'

	def ingresoDengueMes(self, id):
		#anio = datetime.now().year
		anio = 2020
		data=[]		
		for x in range(1,13):			
			deng = Dengue.objects.filter(anio=anio, fec_not__month=x, evento__codigo=id).count()
			data.append(float(deng))		
		return data
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['dengue']=self.ingresoDengueMes(210)
	    context['dengue_grave']=self.ingresoDengueMes(220)
	    context['motalidad_dengue']=self.ingresoDengueMes(580)
	    return context

def dengueList(request):
	#permission_required="den.view_dengue"
	evento = Evento.objects.filter(codigo='210').first()
	dengue = Dengue.objects.filter(evento=evento)
	model = dengue
	titulo = "Listado de paciente con Dengue"
	template_name='den/dengue_list.html'
	contexto = {'obj':dengue, 'titulo':titulo}
	return render(request,template_name, contexto)
	login_url = 'cnf:login'


def dengueGraveList(request):
	#permission_required="den.view_dengue"
	evento = Evento.objects.filter(codigo='220').first()
	dengue = Dengue.objects.filter(evento=evento)
	model = dengue
	titulo = "Listado de paciente con Dengue Grave"
	template_name='den/dengue_list.html'
	#context_object_name = "obj"
	contexto = {'obj':dengue, 'titulo':titulo}
	return render(request,template_name, contexto)
	login_url = 'cnf:login'

def dengueMortalidadList(request):
	#permission_required="den.view_dengue"
	evento = Evento.objects.filter(codigo='580').first()
	dengue = Dengue.objects.filter(evento=evento)
	model = dengue
	titulo = "Listado de Mortalidad por Dengue"
	template_name='den/dengue_list.html'
	#context_object_name = "obj"
	contexto = {'obj':dengue, 'titulo':titulo}
	return render(request,template_name, contexto)
	login_url = 'cnf:login'


def dengueEdit(request, iddengue):
	form = DengueForm()	
	model = Dengue.objects.filter(pk=iddengue).first()
	second_model = SegPacDengue.objects.filter(dengue=model)
	fileden = FilePacDengue.objects.filter(dengue=model)
	iecdengue = IecDengue.objects.filter(dengue=model).first()
	contexto = {'dengue':model, 'segdengue':second_model, 'fileden':fileden, 'iecdengue':iecdengue}	
	template='den/dengue_form.html'
	return render(request,template, contexto)


class SegPacDengueCreate(Sin_privilegio, generic.CreateView):
	permission_required="den.view_dengue"
	model = SegPacDengue
	template_name = 'den/SegPacDengue_Form.html'
	context_object_name = 'obj'
	form_class = SegPacDengueForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(SegPacDengueCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('iddengue') # El mismo nombre que en tu URL
		deng = Dengue.objects.get(pk=pk)
		context['dengue'] = deng
		context['iddengue'] = pk
		context['paciente'] = "{} Notificado el: {} Semana {} ".format(deng.paciente, deng.fec_not, deng.semana)
		context['hallazgos'] = 'Valor predeterminado'
		return context

	def get_success_url(self):
		id_dengue=self.request.POST['dengue']
		return reverse_lazy('den:dengue_edit', kwargs={'iddengue':id_dengue})


class SegPacDengueEdit(Sin_privilegio, generic.UpdateView):
	permission_required="den.update_segpacdengue"
	model = SegPacDengue
	template_name = 'den/SegPacDengue_Form.html'
	context_object_name = 'obj'
	form_class = SegPacDengueForm
	#success_url = redirect('den:dengue_edit', iddengue=)
	login_url = 'cnf:login'

	def get_success_url(self):

		#id_dengue = self.kwargs['dengue_id']
		id_dengue=self.request.POST['dengue']
		return reverse_lazy('den:dengue_edit', kwargs={'iddengue':id_dengue})
	
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(SegPacDengueEdit,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		segpac = SegPacDengue.objects.get(pk=pk)
		deng = Dengue.objects.get(pk=segpac.dengue.id)
		context['dengue'] = deng
		context['iddengue'] = deng.id
		context['paciente'] = "{} Notificado el: {} Semana {} ".format(deng.paciente, deng.fec_not, deng.semana)
		context['hallazgos'] = 'Valor predeterminado'
		return context

def inactivar_ficha_dengue(request, id):
    dengue = Dengue.objects.filter(pk=id).first()
    template_name = 'den/catalogos_del.html'
    contexto = {}

    if not dengue:
        return redirect('den:dengue_list')


    if request.method == 'GET':
        contexto={'obj':dengue}

    if request.method=='POST':
        dengue.estado = False
        dengue.save()
        return redirect('den:dengue_list')
   
    return render(request, template_name, contexto)


def importarDengue210(request):
	form = ImportFileForm(request.POST or None, request.FILES or None)
	template='den/importdengue210.html'
	#evento = Evento.objects.filter(codigo_in =[210,220,580])
	contexto = {'form':form} 	
	linea=[]
	
	if request.method == 'POST':
		sem = int(request.POST['semepidemiologica'])

	if form.is_valid():
		form.save()
		form = ImportFileForm()
		obj = ImportarFile.objects.get(activated=False)
		with open(obj.file_name.path, 'r') as url:
			df = pd.read_excel(obj.file_name)
			#df = pd.read_excel(url)

			dfnew = df.fillna(value=0)
			
			
			#print(xls.sheet_names) nombre de las pestañas
			#df = xls.parse('Hoja1')			
			for i, row in dfnew.iterrows():
				cod_eve = row['cod_eve']
				tipodoc = row['tip_ide_']
				ident = row['num_ide_']
				nombre1 = row['pri_nom_']
				if row['seg_nom_'] != 0:
					nombre2 = row['seg_nom_']
				else:
					nombre2 = ""
				apel1 = row['pri_ape_']
				if row['seg_ape_'] != 'NONE' and row['seg_ape_'] != 0:
					apel2 = row['seg_ape_']
				else:
					apel2 = ""
				direcc = row['dir_res_']
				tel = row['telefono_']
				fecha_nac = datetime.strptime(row['fecha_nto_'], '%d/%m/%Y')  
				reg = row['tip_ss_']
				epsvar = row['cod_ase_']
				etnia = row['per_etn_']
				area = row['area_']
				sexo = row['sexo_']
				gp_gestan =  int(row['gp_gestan'])

							
				td = Tipodoc.objects.get(codigo=tipodoc)
				regimen = Regimen.objects.get(codigo=reg)				
				ar = Area.objects.get(pk=area)
				sex = Sexo.objects.get(codigo=sexo)
				et = Etnia.objects.get(pk=etnia)
				if epsvar != '0':
					eapb = Eps.objects.filter(codigo=epsvar).first()

				linea.append([cod_eve, td.descripcion, ident, nombre1, apel1, apel2, direcc, tel,fecha_nac, gp_gestan])
			
				pac = Paciente.objects.filter(tipodoc=td).filter(identificacion=ident).first()
				
				if pac:
					pac.nombre1 = nombre1
					pac.nombre2 = nombre2
					pac.apellido1 = apel1
					pac.apellido2 = apel2
					pac.save()
				else:
					pac = Paciente()
					pac.tipodoc_id = td.id
					pac.identificacion = ident
					pac.nombre1 = nombre1
					pac.nombre2 = nombre2
					pac.apellido1 = apel1
					pac.apellido2 = apel2
					pac.direccion = direcc
					pac.telefono = tel
					pac.fechaNac = datetime.strftime(fecha_nac, '%Y-%m-%d')

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
				fec_not = datetime.strptime(row['fec_not'], '%d/%m/%Y')  
				cod_pre = row['cod_pre']
				cod_sub = row['cod_sub']
				edad = row['edad_']

				umed = row['uni_med_']
				umedad = UmEdad.objects.filter(codigo=umed).first()

				ocupa = row['ocupacion_']
				ocupacion = Ocupacion.objects.filter(codigo=ocupa).first()
			
				estrato = row['estrato_']
				gp_discapa = row['gp_discapa']
				gp_desplaz = row['gp_desplaz']
				gp_migrant = row['gp_migrant']
				gp_carcela = row['gp_carcela']
				gp_gestan =  row['gp_gestan']
				sem_ges = row['sem_ges']

				gp_indigen = row['gp_indigen']
				gp_pobicbf = row['gp_pobicbf']
				gp_mad_com = row['gp_mad_com']
				gp_desmovi = row['gp_desmovi']
				gp_psiquia = row['gp_psiquia']
				gp_vic_vio = row['gp_vic_vio']
				gp_otros = row['gp_otros']
				departamentor = row['cod_dpto_r']
				dptor = Departamento.objects.filter(codigo=departamentor).first()
				municipior = row['cod_mun_r']
				mpior = Municipio.objects.filter(codigo=municipior).first()

				fec_con = datetime.strptime(row['fec_con_'], '%d/%m/%Y')  
				ini_sin = datetime.strptime(row['ini_sin_'], '%d/%m/%Y')  

 
				clasIni = row['tip_cas_']
				clasiFinicial = ClasiFinicial.objects.filter(pk=clasIni).first()

				pac_hos = row['pac_hos_']
				fec_hos = datetime.strptime(row['fec_hos_'], '%d/%m/%Y')  

				nit_upgd = row['nit_upgd']
				upgd = Upgd.objects.filter(nitcc=nit_upgd).first()
				fiebre = row['fiebre']
				cefalea = row['cefalea']
				dolrretroo = row['dolrretroo']
				mialgias = row['malgias']
				artralgia = row['artralgia']
				erupcionr = row['erupcionr']
				dolor_abdo = row['dolor_abdo']
				vomito = row['vomito']
				diarrea = row['diarrea']
				somnolenci = row['somnolenci']
				hipotensio = row['hipotensio']
				hepatomeg = row['hepatomeg']
				hem_mucosa = row['hem_mucosa']
				hipotermia = row['hipotermia']
				aum_hemato = row['aum_hemato']
				caida_plaq = row['caida_plaq']
				acum_liqui = row['acum_liqui']
				extravasac = row['extravasac']
				hemorr_hem = row['hemorr_hem']
				choque = row['choque']
				danio_organ = row['daño_organ']
				muesttejid = row['muesttejid']
				clasfin = row['clasfinal']
				clasifinalden = ClasiFinalDen.objects.filter(codigo=clasfin).first()
				conduct = row['conducta']
				conducta = Conducta.objects.filter(codigo=conduct).first()

				even = Evento.objects.filter(codigo=cod_eve).first()

				dengue = Dengue.objects.filter(paciente=pac).filter(semana=sem).filter(evento=even).first()
				if dengue:
					pass
				else:
					dengue = Dengue()					
					dengue.evento = even
					dengue.uc = request.user
					dengue.paciente = pac							
					dengue.fec_not = datetime.strftime(fec_not, '%Y-%m-%d')
					dengue.semana = sem	
					dengue.anio = anio
					dengue.cod_pre = cod_pre	
					dengue.cod_sub = cod_sub
					dengue.edad = edad
					if umedad:
						dengue.umedad = umedad
					if ocupacion:
						dengue.ocupacion = ocupacion
					if regimen:
						dengue.regimen = regimen
					if eapb:
						dengue.eps = eapb
					dengue.estrato = estrato
					dengue.gp_discapa = int(gp_discapa)
					dengue.gp_desplaz = int(gp_desplaz)
					dengue.gp_migrant = int(gp_migrant)
					dengue.gp_carcela = int(gp_carcela)
					dengue.gp_gestan = int(gp_gestan)
					if sem_ges == '0':
						pass
					else:
						dengue.sem_ges = int(sem_ges)

					dengue.gp_indigen = int(gp_indigen)
					dengue.gp_pobicbf = int(gp_pobicbf)
					dengue. gp_mad_com= int(gp_mad_com)
					dengue.gp_desmovi = int(gp_desmovi)
					dengue.gp_psiquia = int(gp_psiquia)
					dengue.gp_vic_vio = int(gp_vic_vio)
					dengue.gp_otros = int(gp_otros)
					if dptor:
						dengue.Departamentor = dptor
					if mpior:
						dengue.municipior = mpior
					
					if clasiFinicial:
						dengue.clasiFinicial = clasiFinicial

					dengue.pac_hos = int(pac_hos)
					if fec_hos =='  -   -':
						pass
					else:
						dengue.fec_hos = datetime.strftime(fec_hos, '%Y-%m-%d')


					if ini_sin =='  -   -':
						pass
					else:
						dengue.ini_sin = datetime.strftime(ini_sin, '%Y-%m-%d')

					if upgd:
						dengue.upgd = upgd
					dengue.fiebre = int(fiebre)
					dengue.cefalea = int(cefalea)
					dengue.dolrretroo = int(dolrretroo)
					dengue.mialgias = int(mialgias)
					dengue.artralgia = int(artralgia)
					dengue.erupcionr = int(erupcionr)
					dengue.dolor_abdo = int(dolor_abdo)
					dengue.vomito = int(vomito)
					dengue.diarrea = int(diarrea)
					dengue.somnolenci = int(somnolenci)
					dengue.hipotensio = int(hipotensio)
					dengue.hepatomeg = int(hepatomeg)
					dengue.hem_mucosa = int(hem_mucosa)
					dengue.hipotermia = int(hipotermia)
					dengue.aum_hemato = int(aum_hemato)
					dengue.caida_plaq = int(caida_plaq)
					dengue.acum_liqui = int(acum_liqui)
					dengue.extravasac = int(extravasac)
					dengue.hemorr_hem = int(hemorr_hem)
					dengue.choque = int(choque)
					dengue.danio_organ = int(danio_organ)
					dengue.muesttejid = int(muesttejid)
					if clasifinalden:
						dengue.clasifinalden = clasifinalden
					if conducta:
						dengue.conducta = conducta
					dengue.save() 
				
			contexto.update({'dfc':linea})		

					#-----------------------------"""

		obj.activated = True
		obj.save()
		return redirect('den:dengue_list')

	return render(request,template, contexto)
