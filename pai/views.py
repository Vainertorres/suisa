from django.views import generic
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django_pandas.io import read_frame

import folium
from folium.plugins import MarkerCluster
import pandas as pd 
import seaborn as sns
import webbrowser
from io import BytesIO
import base64

from .models import VacunaCovid, RediarioCargado, Rediario
from aseg.models import Maestrosub, Maestrocont 
from .forms import ImportFileForm, RediarioCreateForm
from cnf.views import Sin_privilegio
from cnf.models import Tipodoc

# Create your views here.

class RediarioPrint(Sin_privilegio, generic.ListView):
	permission_required="pai.view_Rediario"
	model=Rediario
	paginate_by=100
	context_object_name = "obj"
	template_name='pai/rediario_print.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		idrediario = self.kwargs.get('id') # El mismo nombre que en tu URL
		pacvacunado = Rediario.objects.filter(pk=idrediario)
		userVac = Rediario.objects.filter(pk=idrediario).first()
		context['usuario'] = pacvacunado
		context['codeqr'] = str(userVac.fecha) + ' ' + userVac.razonsocial + \
		' ' +userVac.dosisaplicada + ' ' + userVac.laboratorio
		return context


class GrafLaborartio(generic.TemplateView):
	template_name='pai/estpaigrupopriorizadoform.html'

	def reporteGrupoPriorizado(self):
		grupo = Rediario.objects.values('laboratorio').annotate(Count('id')).order_by('laboratorio')
		diccionario = {}
		data = []
		for x in grupo:			
			diccionario = {'name':x['laboratorio'],'y':x['id__count']}
			data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    dato = self.reporteGrupoPriorizado()
	   # print("dato primera posiscion", dato[0])
	    context['panel']='Panel de Administrador'
	    context['labo']= dato
	    return context


class GrafVacunaIps(generic.TemplateView):
	template_name='pai/estPaipsform.html'

	def reportePaIps(self):		
		listips = Rediario.objects.values('nombreIps').annotate(Count('id')).order_by('nombreIps')
		diccionario = {}
		data = []
		for x in listips:
			
			diccionario = {'name':x['nombreIps'],'y':x['id__count']}
			data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['ips']= self.reportePaIps()
	    return context


class GrafTipoPoblacion(generic.TemplateView):
	template_name='pai/estPaitipopoblacionform.html'

	def reporteTipopob(self):
		qs = Rediario.objects.values('tipopoblacion').annotate(Count('id')).order_by('-id__count')[0:20]
		diccionario = {}
		data = []
		for x in qs:
			diccionario = {'name':x['tipopoblacion'],'y':x['id__count']}
			data.append(diccionario)
		return data


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context = super().get_context_data(**kwargs)
		context['panel']='Panel de Administrador'
		context['tipob']= self.reporteTipopob()
		return context
			


class GrafTipoSexo(generic.TemplateView):
	template_name='pai/estPaitiposexoform.html'

	def reporteTipoSexo(self):
		qs = Rediario.objects.values('sexo').annotate(Count('id')).order_by('-id__count')
		diccionario = {}
		data = []
		for x in qs:
			diccionario = {'name':x['sexo'],'y':x['id__count']}
			data.append(diccionario)
		return data


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context = super().get_context_data(**kwargs)
		context['panel']='Panel de Administrador'
		context['tiposexo']= self.reporteTipoSexo()
		return context


class GrafVacunaEtapa(generic.TemplateView):
	template_name='pai/estPaiEtapaform.html'

	def reporteEtapa(self):		
		listetapa = Rediario.objects.values('etapa').annotate(Count('id')).order_by('etapa')
		diccionario = {}
		data = []
		for x in listetapa:
			
			diccionario = {'name':x['etapa'],'y':x['id__count']}
			data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['etapa']= self.reporteEtapa()
	    return context


class GrafVacunaModalidad(generic.TemplateView):
	template_name='pai/estPaModaldiadform.html'

	def reporteModalidad(self):		
		listmodalidad = Rediario.objects.values('modalidad').annotate(Count('id')).order_by('modalidad')
		diccionario = {}
		data = []
		for x in listmodalidad:
			
			diccionario = {'name':x['modalidad'],'y':x['id__count']}
			data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['modalidad']= self.reporteModalidad()
	    return context

class GrafPaiDosisAplicadas(generic.TemplateView):
	template_name='pai/estpaidosisaplicadasform.html'
	

	def reportePaiDosisprimera(self, dato):
		
		if dato == 1:
			dosis = Rediario.objects.filter(dosisaplicada='1 = Primera Dosis').count()
		if dato == 2:
			dosis = Rediario.objects.filter(dosisaplicada='2 = Segunda Dosis').count()
		if dato == 3:
			dosis = Rediario.objects.filter(dosisaplicada='3 = Única').count()
		if dato == 4:
			dosis = Rediario.objects.filter(dosisaplicada='4 = Refuerzo').count()
		if dato == 5:
			dosis = Rediario.objects.filter(dosisaplicada='5 = SEGUNDO REFUERZO').count()
		return float(dosis)
			
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['panel']='Panel de Administrador'
				
		context['primeras']=self.reportePaiDosisprimera(1)
		context['segundas']= self.reportePaiDosisprimera(2)
		context['unica']= self.reportePaiDosisprimera(3)
		context['refuerzo']= self.reportePaiDosisprimera(4)
		context['sgdorefuerzo']= self.reportePaiDosisprimera(5)
		return context


class RediarioList(Sin_privilegio, generic.ListView):
	permission_required="pai.view_Rediario"
	model=Rediario
	paginate_by=100
	context_object_name = "obj"
	template_name='pai/rediario_list.html'
	#login_url = 'cnf:login'


	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):		
		accion = request.POST.get("action", "searchdata")	
		print('Trayendo datos ',accion)
		try:
			
			#only('id','fecha','tipodoc', 'identificacion', 'razonsocial', \
			#'edad','telefono','eapb','tipopoblacion', 'laboratorio','dosisaplicada', 'nombreIps')
			#action = request.POST["action"]
			
			if accion == 'searchdata':
				data = []
				
				for i in Rediario.objects.all():
					data.append(i.toJSON())
			else:
				data['error'] = 'Ha ocurrido un error'

		except Exception as e:
			print('Ocurrio un error')
			data['error']=str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de rediarios'
		context['create_url'] = reverse_lazy('pai:rediario_new')
		context['list_url'] = reverse_lazy('pai:rediario_list')
		context['entity'] = 'Rediarios'
		return context



class RediarioListAjax(Sin_privilegio, generic.ListView):
	permission_required="pai.view_Rediario"
	#if request.is_ajax():
	model = Rediario
	paginate_by = 100
	template_name='pai/rediario_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'

class RediarioCreate(Sin_privilegio, generic.CreateView):
	permission_required="pai.add_Rediario"
	model = Rediario
	template_name = 'pai/rediariocreateform.html'
	context_object_name = 'obj'
	form_class = RediarioCreateForm	
	success_url = reverse_lazy('pai:rediario_list')	
	login_url = 'cnf:login'

class RediarioUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="pai.change_Rediario"
	model = Rediario
	template_name = 'pai/rediariocreateform.html'
	context_object_name = 'obj'
	form_class = RediarioCreateForm	
	success_url = reverse_lazy('pai:rediario_list')		
	login_url = 'cnf:login'

def importarRediarios(request):
	form = ImportFileForm(request.POST or None, request.FILES or None)
	template='pai/importrediarios.html'	
	contexto = {'form':form} 	
	linea=[]	

	if form.is_valid():
		form.save()
		form = ImportFileForm()
		obj = RediarioCargado.objects.get(activated=False)
		with open(obj.file_name.path, 'r') as url:
			df = pd.read_excel(obj.file_name)
			dfnew = df.fillna(value=0)
			#tqdm(dfnew.shape())
			
			for i, row in dfnew.iterrows():
				if i >= 1:
					print(f"linea {i}")
					fechaapli = row['FechaVac']
					tipodoc = row['Tipodoc'].strip() #Eliminar caracteres en blanco al inicio y final
					if row['Tipodoc'] != 'NONE' and row['Tipodoc'] != "0":
						td = Tipodoc.objects.filter(codigo = tipodoc).first()

					ident = str(row['identificacion'])
					fechanac = row['FechaNac']
					tipoedad = row['Tipoedad']
					edad = row['edad']
					sexo = row['sexo']
					
					apel1 = row['Apellido1']
					if row['Apellido2'] != 'NONE' and row['Apellido2'] != "0":
						apel2 = row['Apellido2']
					else:
						apel2 = ""
					nombres = row['Nombres']
					regimen = row['Regimen']
					aseguradora = row['Aseguradora']
					departamentoRes = row['DepartamentoResidencia']
					municipioRes = row['MunicipioResidencia']
					area = row['Area']
					barrio = row['Barrio']
					direcc = row['Direccion']
					tel = row['Telefono']
					etnia = row['Etnia']
					desplazado = row['Desplazado']
					discapacitado =  row['Discapacitado']
					email = row['Email']
					condiccUsuaria =  row['CondiccUsuaria']
					fpp = row['FechaPP']
					if isinstance(fpp, str):
						fpp = fpp.strip()
					
					fechaPP = fpp #Hacer validacion tipo de dato para eliminar caracteres vacios
					etapa = row['EtapaVacunacion']
					tipoPoblacion = row['TipoPoblacion']
					dosis = row['Dosis']
					laboratorio = row['Laboratorio']
					loteBiologico = row['LoteBiologico']
					jeringa = row['Jeringa']
					loteJeringa = row['LoteJeringa']
					eventoadverso = row['Eventoadverso']
					nameVacunador = row['NameVacunador']
					municipioreporta = row['Municipioreporta']
					nombreIPS = row['NombreIPS']
					novedad = row['Novedad']
					descNovedad = row['DescNovedad']
					modalidad = row['Modalidad']

					
					red = Rediario.objects.filter(fecha=fechaapli).filter(tipodoc=tipodoc).filter(identificacion=ident).first()

					if not red:
						linea.append([fechaapli,tipodoc, ident,fechanac,tipoedad, edad,sexo, apel1, apel2, nombres,aseguradora,departamentoRes, \
						municipioRes, area,barrio, direcc, tel, etnia, desplazado,discapacitado,email, \
						condiccUsuaria, fechaPP, etapa, tipoPoblacion, dosis, laboratorio, jeringa, loteJeringa, \
						eventoadverso, nameVacunador, municipioreporta, nombreIPS, novedad, descNovedad, modalidad])						
						red = Rediario()
						red.fecha = fechaapli
						red.tipodoc = tipodoc
						red.identificacion = ident.strip()
						nomeps=""
						objmaestro = Maestrosub.objects.filter(tipodoc=td).filter(identificacion=red.identificacion).first()
						if objmaestro:
							red.regimen = '2 = Subsidiado'
						else:
							objmaestro = Maestrocont.objects.filter(tipodoc=td).filter(identificacion=red.identificacion).first()
							if objmaestro:					
								red.regimen = '1 = Contributivo'						

						if objmaestro:
							red.eapb = objmaestro.eps.descripcion
							red.fechanac = objmaestro.fechanac

						else:
							red.regimen = regimen 					
							red.fechanac = fechanac
							red.eapb = aseguradora
						
						red.tipoedad = tipoedad
						red.edad = edad
						red.sexo = sexo
						red.apellido1 = apel1
						red.apellido2 = apel2
						red.nombres = nombres					
											
						red.departamentores = departamentoRes
						red.municipiores = municipioRes 
						red.area = area
						red.barrio = barrio 
						red.direccion =	direcc
						red.telefono = tel 
						red.grupoetnico = etnia
						red.desplazado = desplazado
						red.discapacitado = discapacitado
						red.correoelectronico =	email
						red.condiccusuaria = condiccUsuaria
						if fechaPP != 0:
							red.fechaprobparto = fechaPP
						red.etapa =	etapa
						red.tipopoblacion = tipoPoblacion
						red.dosisaplicada = dosis
						red.laboratorio = laboratorio 
						red.lotebiologico = loteBiologico
						red.jeringa = jeringa
						red.lotejeringa = loteJeringa
						red.eventoadverso = eventoadverso
						red.vacunador = nameVacunador
						red.municipio = municipioreporta 
						red.nombreIps = nombreIPS
						red.novedad = novedad
						red.descNovedad = descNovedad
						red.modalidad = modalidad
						red.observacion = ""
						red.reportado = 'SI'
						red.save()

			contexto.update({'dfc':linea})		

		obj.activated = True
		obj.save()
		return redirect('pai:rediario_list')

	return render(request,template, contexto) 
