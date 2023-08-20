from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from cnf.views import Sin_privilegio
from django.views import generic
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum

import folium
from folium.plugins import MarkerCluster
import webbrowser

# Create your views here.
from cnf.models import SemEpidemiologica, CondiccionFinal, Paciente, Departamento, Municipio, \
Sexo, Etnia, Evento, Eps, Regimen, ClasiFinicial, UmEdad, Ocupacion, Tipodoc, Upgd, Pais, Area, Barrio

from bai.models import Diagnosticos 


from lab.models import TipoExamen

from .models import ImportarMalaria, Malaria, Tratamiento, EspecieInf, SegPacMalaria, Conglomerado, \
ConglomeradoMalaria, SegCongloMalaria,FileConglomerado
from .forms import ImportFileForm, MalariaForm, SegPacMalariaForm, ConglomeradoMalariaForm, \
PacienteCongloMalariaForm, SegConglomeradoMalariaForm, FileConglomeradoForm
import pandas as pd
from datetime import date
from datetime import datetime

class GrafMalariaBarrio(generic.TemplateView):
	template_name='mlr/estmalariabarrio_form.html'

	def reporteMalariaBarrio(self):

		barrios = Barrio.objects.all()
		
		diccionario = {}
		data = []
		for x in barrios:
			cantbarrio = Malaria.objects.filter(paciente__barrio_id = x.id).count()
			if cantbarrio > 0:
				diccionario = {'name':x.descripcion,'y':cantbarrio}
				data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['barrio']= self.reporteMalariaBarrio()
	    return context

class GrafMalariaEPS(generic.TemplateView):
	template_name='mlr/estmalariaeps_form.html'

	def reporteMalariaEPS(self):
		eps = Eps.objects.all()
		diccionario = {}
		data = []
		for x in eps:
			canteps = Malaria.objects.filter(paciente__eps_id = x.id).count()
			if canteps > 0:
				diccionario = {'name':x.descripcion,'y':canteps}
				data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['eps']= self.reporteMalariaEPS()
	    return context



class GrafMalariaSemEpi(generic.TemplateView):
	template_name='mlr/estmlrsemepidemiologica.html'
	
	

	def ingresos_malaria(self, id):
		anio = datetime.now().year
		mlrmax = Malaria.objects.all().aggregate(Max('semana'))
		rangofin=mlrmax['semana__max']
		rangofin+=1
		data=[]		
		for x in range(1, rangofin):	
			malaria = Malaria.objects.filter(anio=anio, semana=x).count()
			data.append(float(malaria))		
		return data

	def rango_fin(self):
		mlrmax = Malaria.objects.all().aggregate(Max('semana'))
		rangofin=mlrmax['semana__max']
		return rangofin

	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['malaria']=self.ingresos_malaria(1)
	    context['rangoini']=1
	    context['rangofin']=self.rango_fin()
	    return context

class GrafComplicacionMlr(generic.TemplateView):
	template_name='mlr/estcomplicaciones_form.html'

	def cantComplicados(self, id):
		#anio = datetime.now().year
		data=[]		
		if id==1:
			malaria = Malaria.objects.filter(complicaci='1').filter(com_cerebr='1').count()
		if id==2:
			malaria = malaria = Malaria.objects.filter(complicaci='1').filter(com_renal='1').count()			
		if id==3:
			malaria = malaria =  Malaria.objects.filter(complicaci='1').filter(com_hepati='1').count()	
		if id==4:
			malaria = Malaria.objects.filter(complicaci='1').filter(com_pulmon='1').count()
		if id==5:
			malaria = Malaria.objects.filter(complicaci='1').filter(com_hemato='1').count()
		if id==6:
			malaria = Malaria.objects.filter(complicaci='1').filter(com_otras='1').count()
			
		data.append(float(malaria))		
		return data
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['cerebro']=self.cantComplicados(1)
	    context['renal']=self.cantComplicados(2)
	    context['hepatica']=self.cantComplicados(3)
	    context['pulmon']=self.cantComplicados(4)
	    context['hemato']=self.cantComplicados(5)
	    context['otras']=self.cantComplicados(6)
	    return context



def geolocMapaCalorMalaria(request):
	malaria = Malaria.objects.filter(~Q(paciente__lat='SD')).filter(~Q(paciente__lon='SD')).values('paciente__identificacion','paciente__lat','paciente__lon')
	
	some_map2 = folium.Map(location=[2.772107,-77.666511], zoom_start = 10)
	mc = MarkerCluster()


	for row in malaria:
		lat = row['paciente__lat']
		lon = row['paciente__lon']
		ident = row['paciente__identificacion']
		mc.add_child(folium.Marker(location=[lat, lon], popup=ident))

	some_map2.add_child(mc)

	filepath = 'C:/mapas/mapacalor.html'
	some_map2.save(filepath)
	webbrowser.open('file://' + filepath)
	html_string = some_map2.get_root().render()
	context = {'sm':some_map2, 'malaria':malaria, 'hs':html_string}

	return redirect('mlr:malaria_list')


def geolocMalaria(request):	
	malaria = Malaria.objects.filter(~Q(paciente__lat='SD')).filter(~Q(paciente__lon='SD')).values('paciente__identificacion','paciente__lat','paciente__lon')
	
	some_map = folium.Map(location=[2.772107,-77.666511], zoom_start = 15)
	
	for row in malaria:
		lat = row['paciente__lat']
		lon = row['paciente__lon']
		ident = row['paciente__identificacion']
		some_map.add_child(folium.Marker(location=[lat, lon], popup=ident))

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'malaria':malaria, 'hs':html_string}

	return redirect('mlr:malaria_list')


class ConglomeradoMalariaList(Sin_privilegio, generic.ListView):
    permission_required="mlr.view_conglomerado"
    model = Conglomerado
    template_name='mlr/conglomeradomalaria_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class ConglomeradoMalariaCreate(Sin_privilegio, generic.CreateView):
	permission_required="mlr.add_conglomerado"
	model = Conglomerado
	template_name = 'mlr/conglomeradomalaria_form.html'
	context_object_name = 'obj'
	form_class = ConglomeradoMalariaForm
	success_url = reverse_lazy('mlr:conglomeradomlr_list')
	login_url = 'cnf:login'    


class ConglomeradoMalariaEdit(Sin_privilegio, generic.UpdateView):
	permission_required="mlr.change_conglomerado"
	model = Conglomerado
	template_name = 'mlr/conglomeradomalaria_form.html'
	context_object_name = 'obj'
	form_class = ConglomeradoMalariaForm
	success_url = reverse_lazy('mlr:conglomeradomlr_list')
	login_url = 'cnf:login' 

	def get_context_data(self, **kwargs):
		context = super(ConglomeradoMalariaEdit,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		conglomeradomalaria = ConglomeradoMalaria.objects.filter(conglomerado_id=pk)
		segconglo = SegCongloMalaria.objects.filter(conglomerado_id=pk)
		fileconglo = FileConglomerado.objects.filter(conglomerado_id=pk)
		context['cm'] = conglomeradomalaria		
		context['segconglo'] = segconglo	
		context['fileconglo'] = fileconglo		
			
		return context

class MalariaList(Sin_privilegio, generic.ListView):
	permission_required="mlr.view_malaria"
	model = Malaria
	template_name='mlr/malaria_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'

def malariaEdit(request, idmalaria):
	form = MalariaForm()	
	model = Malaria.objects.filter(pk=idmalaria).first()
	segpacmalaria = SegPacMalaria.objects.filter(malaria=model)
	#fileden = FilePacDengue.objects.filter(dengue=model)
	#iecdengue = IecDengue.objects.filter(dengue=model).first()
	contexto = {'malaria':model, 'segmlr':segpacmalaria}
	template='mlr/malaria_form.html'
	return render(request,template, contexto)	


class SegConglomeradoMalariaCreate(Sin_privilegio, generic.CreateView):
	permission_required="mlr.add_segconglomalaria"
	model = SegCongloMalaria
	template_name = 'mlr/segconglomeradomalaria_form.html'
	context_object_name = 'obj'
	form_class = SegConglomeradoMalariaForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	
	def get_context_data(self, **kwargs):
		context = super(SegConglomeradoMalariaCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idconglomerado') # El mismo nombre que en tu URL
		conglo = Conglomerado.objects.get(pk=pk)
		context['conglomerado'] = conglo
		context['idconglomerado'] = pk		
		return context

	def get_success_url(self):
		idconglo=self.request.POST['conglomerado']
		return reverse_lazy('mlr:conglomeradomlr_edit', kwargs={'pk':idconglo})


class SegConglomeradoMalariaUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="mlr.change_segconglomalaria"
	model = SegCongloMalaria
	template_name = 'mlr/segconglomeradomalaria_form.html'
	context_object_name = 'obj'
	form_class = SegConglomeradoMalariaForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	
	def get_context_data(self, **kwargs):
		context = super(SegConglomeradoMalariaUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		segconglo = SegCongloMalaria.objects.filter(pk=pk).first()
		conglo = Conglomerado.objects.get(pk=segconglo.id)
		context['conglomerado'] = conglo
		context['idconglomerado'] = conglo.id		
		return context

	def get_success_url(self):
		idconglo=self.request.POST['conglomerado']
		return reverse_lazy('mlr:conglomeradomlr_edit', kwargs={'pk':idconglo})


class FileConglomeradoCreate(Sin_privilegio, generic.CreateView):
	permission_required="mlr.add_fileconglomerado"
	model = FileConglomerado
	template_name = 'mlr/fileconglomerado_form.html'
	context_object_name = 'obj'
	form_class = FileConglomeradoForm	
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(FileConglomeradoCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idconglomerado') # El mismo nombre que en tu URL
		conglo = Conglomerado.objects.get(pk=pk)
		context['conglomerado'] = conglo
		context['idconglomerado'] = pk				
		return context

	def get_success_url(self):
		idconglo=self.request.POST['conglomerado']
		return reverse_lazy('mlr:conglomeradomlr_edit', kwargs={'pk':idconglo})

class FileConglomeradoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="mlr.change_fileconglomerado"
	model = FileConglomerado
	template_name = 'mlr/fileconglomerado_form.html'
	context_object_name = 'obj'
	form_class = FileConglomeradoForm	
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(FileConglomeradoUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		filconglo = FileConglomerado.objects.filter(pk=pk).first()
		conglo = Conglomerado.objects.get(pk=filconglo.id)
		context['conglomerado'] = conglo
		context['idconglomerado'] = conglo.id			
		return context

	def get_success_url(self):
		idconglo=self.request.POST['conglomerado']
		return reverse_lazy('mlr:conglomeradomlr_edit', kwargs={'pk':idconglo})

class SegPacMalariaCreate(Sin_privilegio, generic.CreateView):
	permission_required="mlr.add_segpacmalaria"
	model = SegPacMalaria
	template_name = 'mlr/segpacmalaria_form.html'
	context_object_name = 'obj'
	form_class = SegPacMalariaForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	
	def get_context_data(self, **kwargs):
		context = super(SegPacMalariaCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idmalaria') # El mismo nombre que en tu URL
		mlr = Malaria.objects.get(pk=pk)
		context['malaria'] = mlr
		context['idmalaria'] = pk
		context['paciente'] = "{} Notificado el: {} Semana {} ".format(mlr.paciente, mlr.fec_not, mlr.semana)
		context['hallazgos'] = 'Valor predeterminado'
		return context

	def get_success_url(self):
		id_malaria=self.request.POST['malaria']
		return reverse_lazy('mlr:malaria_edit', kwargs={'idmalaria':id_malaria})


class SegPacMalariaEdit(Sin_privilegio, generic.UpdateView):
	permission_required="mlr.update_segpacmalaria"
	model = SegPacMalaria
	template_name = 'mlr/segpacmalaria_form.html'
	context_object_name = 'obj'
	form_class = SegPacMalariaForm
	#success_url = redirect('den:dengue_edit', iddengue=)
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(SegPacMalariaEdit,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		segpac = SegPacMalaria.objects.get(pk=pk)
		mlr = Malaria.objects.get(pk=segpac.malaria.id)
		context['malaria'] = mlr
		context['idmalaria'] = mlr.id
		context['paciente'] = "{} Notificado el: {} Semana {} ".format(mlr.paciente, mlr.fec_not, mlr.semana)
		context['hallazgos'] = 'Valor predeterminado'
		return context

	def get_success_url(self):
		id_malaria=self.request.POST['malaria']
		return reverse_lazy('mlr:malaria_edit', kwargs={'idmalaria':id_malaria})

class ConglomeradoPacMalariaCreate(Sin_privilegio, generic.CreateView):
	permission_required="mlr.add_conglomeradomalaria"
	model = ConglomeradoMalaria
	template_name = 'mlr/conglomeradopacmalaria_form.html'

	context_object_name = 'obj'
	form_class = PacienteCongloMalariaForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	
	def get_context_data(self, **kwargs):
		context = super(ConglomeradoPacMalariaCreate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('idconglomerado') # El mismo nombre que en tu URL
		conglo = Conglomerado.objects.get(pk=pk)
		context['conglo'] = conglo
		context['idconglomerado'] = pk
		return context

	def get_success_url(self):
		id_conglomerado=self.request.POST['conglomerado']
		return reverse_lazy('mlr:conglomeradomlr_edit', kwargs={'pk':id_conglomerado})


class ConglomeradoPacMalariaUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="mlr.change_conglomeradomalaria"
	model = ConglomeradoMalaria
	template_name = 'mlr/conglomeradopacmalaria_form.html'
	context_object_name = 'obj'
	form_class = PacienteCongloMalariaForm
	#success_url = reverse_lazy('den:dengue_edit', kwargs={'iddengue':dengue_id} )
	login_url = 'cnf:login'

	
	def get_context_data(self, **kwargs):
		context = super(ConglomeradoPacMalariaUpdate,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL
		paconglo = ConglomeradoMalaria.objects.get(pk=pk)
		conglo = Conglomerado.objects.filter(pk=paconglo.conglomerado.id).first()
		context['conglo'] = conglo
		context['idconglomerado'] = conglo.id		
		return context

	def get_success_url(self):
		id_conglomerado=self.request.POST['conglomerado']
		return reverse_lazy('mlr:conglomeradomlr_edit', kwargs={'pk':id_conglomerado})


def importarMalaria(request):
	form = ImportFileForm(request.POST or None, request.FILES or None)
	template='mlr/importmalaria.html'	
	contexto = {'form':form} 	
	linea=[]
	
	if request.method == 'POST':
		sem = int(request.POST['semepidemiologica'])

	if form.is_valid():
		form.save()
		form = ImportFileForm()
		obj = ImportarMalaria.objects.get(activated=False)
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
				nombre1 = row['pri_nom_']
				if row['seg_nom_'] != 0:
					nombre2 = row['seg_nom_']
				apel1 = row['pri_ape_']
				if row['seg_ape_'] != 'NONE' and row['seg_ape_'] != 0:
					apel2 = row['seg_ape_']
				else:
					apel2 = ""
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
				regimen = Regimen.objects.get(codigo=reg)				
				ar = Area.objects.get(codigo=area)
				sex = Sexo.objects.get(codigo=sexo)
				et = Etnia.objects.get(pk=etnia)
				if epsvar != '0':
					eapb = Eps.objects.filter(codigo=epsvar).first()

				linea.append([cod_eve, td.descripcion, ident, nombre1, apel1, apel2, direcc, tel,fecha_nac])
			
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
				cod_pre = row['cod_pre']
				cod_sub = row['cod_sub']
				edad = row['edad_']
				sem = row['semana']
				cod_eve = row['cod_eve']

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
				sem_ges = row['sem_ges_']

				gp_indigen = row['gp_indigen']
				gp_pobicbf = row['gp_pobicbf']
				gp_mad_com = row['gp_mad_com']
				gp_desmovi = row['gp_desmovi']
				gp_psiquia = row['gp_psiquia']
				gp_vic_vio = row['gp_vic_vio']
				gp_otros = row['gp_otros']
				idcod_pais_r = row['cod_pais_r']
				cod_pais_r = Pais.objects.filter(codigo=idcod_pais_r).first()
				departamentor = int(row['cod_dpto_r'])
				dptor = Departamento.objects.filter(codigo=departamentor).first()
				municipior = int(row['cod_mun_r'])
				mpior = Municipio.objects.filter(codigo=municipior).first()
				fec_con = row['fec_con_']
				ini_sin = row['ini_sin_']
				clasIni = row['tip_cas_']
				clasiFinicial = ClasiFinicial.objects.filter(pk=clasIni).first()
				pac_hos = row['pac_hos_']
				fec_hos = row['fec_hos_']				
				con_fin = row['con_fin_']
				condiccFinal = CondiccionFinal.objects.filter(codigo=con_fin).first()
				fec_def = row['fec_def_']
				ajuste = row['ajuste_']
				fec_aju = row['fec_aju_']
				cer_def = row['cer_def_']
				cbmte = row['cbmte_']
				cie10 = Diagnosticos.objects.filter(codigo=cbmte).first()
				vig_activa = row['vig_activa']
				sintomatic = row['sintomatic']
				clas_caso = row['clas_caso']
				recrudece = row['recrudece']
				trimestre = row['trimestre']
				idtipoexamen = row['tipoexamen']
				tipoexamen = TipoExamen.objects.filter(codigo=idtipoexamen).first()				
				recuento = row['recuento']
				gametocito = row['gametocito']
				desplazami = row['desplazami']
				iddespla_codpais =row['despla_codpais']
				despla_codpais = Pais.objects.filter(descripcion=iddespla_codpais).first()
				iddespla_coddep = row['despla_coddep']
				despla_coddep = Departamento.objects.filter(descripcion=iddespla_coddep).first()
				iddespla_codmun = row['despla_codmun']
				despla_codmun = Municipio.objects.filter(descripcion=iddespla_codmun).first()
				complicaci = row['complicaci']
				com_cerebr = row['com_cerebr']
				com_renal = row['com_renal']
				com_hepati = row['com_hepati']
				com_pulmon = row['com_pulmon']
				com_hemato = row['com_hemato']
				com_otras = row['com_otras']
				idtrata = row['tratamient']
				tratamient = Tratamiento.objects.filter(codigo=idtrata).first()
				f_ini_trat = row['f_ini_trat']				
				idespecieinf = row['esp_pla']
				especieinf = EspecieInf.objects.filter(codigo=idespecieinf).first()
				resp_diag= row['resp_diag']
				fec_result= row['fec_result']
				result_exa = row['result_exa']
				nuevo = row['nuevo']
				nom_upgd = row['nom_upgd']
				nompais_proce = row['npais_proce']
				npais_proce = Pais.objects.filter(descripcion=nompais_proce).first()
				nomdep_proce = row['ndep_proce']
				ndep_proce = Departamento.objects.filter(descripcion=nomdep_proce).first()
				nommun_proce = row['nmun_proce']
				nmun_proce = Municipio.objects.filter(descripcion=nommun_proce).first()
				even = Evento.objects.filter(codigo=cod_eve).first()
				nit_upgd = row['nit_upgd']
				upgd = Upgd.objects.filter(nitcc=nit_upgd).first()

				# -----

				malaria = Malaria.objects.filter(paciente=pac).filter(semana=sem).filter(evento=even).first()
				if malaria:
					pass
				else:
					malaria = Malaria()					
					malaria.evento = even					
					malaria.paciente = pac		
					malaria.fec_not = fec_not	
					malaria.semana = sem	
					malaria.anio = anio
					malaria.cod_pre = cod_pre	
					malaria.cod_sub = cod_sub
					malaria.edad = edad
					if umedad:
						malaria.umedad = umedad
					if ocupacion:
						malaria.ocupacion = ocupacion
					if regimen:
						malaria.regimen = regimen
					if eapb:
						malaria.eps = eapb
					malaria.estrato = estrato
					malaria.gp_discapa = int(gp_discapa)
					malaria.gp_desplaz = int(gp_desplaz)
					malaria.gp_migrant = int(gp_migrant)
					malaria.gp_carcela = int(gp_carcela)
					malaria.gp_gestan = int(gp_gestan)
					if sem_ges == '0':
						pass
					else:
						malaria.sem_ges = int(sem_ges)

					malaria.gp_indigen = int(gp_indigen)
					malaria.gp_pobicbf = int(gp_pobicbf)
					malaria. gp_mad_com= int(gp_mad_com)
					malaria.gp_desmovi = int(gp_desmovi)
					malaria.gp_psiquia = int(gp_psiquia)
					malaria.gp_vic_vio = int(gp_vic_vio)
					malaria.gp_otros = int(gp_otros)
					if cod_pais_r:
						malaria.paisr = cod_pais_r
					if dptor:
						malaria.Departamentor = dptor
					if mpior:
						malaria.municipior = mpior
					
					if clasiFinicial:
						malaria.clasiFinicial = clasiFinicial

					malaria.pac_hos = int(pac_hos)
					if fec_hos =='  -   -':
						pass
					else:
						malaria.fec_hos = fec_hos

					if ini_sin =='  -   -':
						pass
					else:
						malaria.ini_sin = ini_sin

					if upgd:
						malaria.upgd = upgd
					
					if condiccFinal:
						malaria.condiccionfinal = condiccFinal

					if fec_def =='  -   -':
						pass
					else:
						malaria.fec_def = fec_def
					malaria.ajuste = ajuste

					if fec_aju =='  -   -':
						pass
					else:
						malaria.fec_ajuste = fec_aju
					malaria.cer_def = cer_def
					if cie10:
						malaria.malaria.cbmte = cie10
					malaria.telefono = tel					
					malaria.nit_upgd = nit_upgd
					
					malaria.vig_activa = int(vig_activa)
					malaria.sintomatic = int(sintomatic)
					malaria.clas_caso = int(clas_caso)
					malaria.recrudece = int(recrudece)
					malaria.trimestre = int(trimestre)
					if tipoexamen:
						malaria.tipoexamen = tipoexamen
					malaria.recuento = recuento
					malaria.gametocito = int(gametocito)
					malaria.desplazami = int(desplazami)
					if despla_codpais:
						malaria.despla_codpais = despla_codpais
					if despla_coddep:
						malaria.despla_coddep = despla_coddep
					if despla_codmun:
						malaria.despla_codmun = despla_codmun
					malaria.complicaci = int(complicaci)
					malaria.com_cerebr = int(com_cerebr)
					malaria.com_renal = int(com_renal)
					malaria.com_hepati = int(com_hepati)
					malaria.com_pulmon = int(com_pulmon)
					malaria.com_hemato = int(com_hemato)
					malaria.com_otras = int(com_otras)
					if tratamient:
						malaria.tratamiento = tratamient
					if f_ini_trat =='  -   -':
						pass
					else:
						malaria.f_ini_trat = f_ini_trat

					if especieinf:
						malaria.especieinf = especieinf
					malaria.resp_diag = resp_diag
					if fec_result =='  -   -':
						pass
					else:
						malaria.fec_result = fec_result
					malaria.result_exa = result_exa
					malaria.nuevo = int(nuevo)
					malaria.nom_upgd = nom_upgd
					if npais_proce:
						malaria.npais_proce = npais_proce.id
					if ndep_proce:
						malaria.ndep_proce = ndep_proce.id
					if nmun_proce:
						malaria.nmun_proce = nmun_proce.id			
			
					malaria.save() 
				
			contexto.update({'dfc':'Prueba'})		

					#-----------------------------"""

		obj.activated = True
		obj.save()
		return redirect('mlr:malaria_list')

	return render(request,template, contexto)
