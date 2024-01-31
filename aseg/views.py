import csv
from django.http import HttpResponse
from django.contrib import messages

from django.views import generic
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pandas as pd
from datetime import datetime
from tqdm import tqdm

from cnf.views import Sin_privilegio
from .models import Maestrosub, MaestrobduaCargado, Tipopoblacionesp, Metodologiagp, Parentezcocf, \
Nivelsisben, Metodologiagp, Condiciondiscapacidad, Resguardo, Maestrocont, Tipocontizante, \
Tipoafiliado, RepNovedad, Formularioafil, Sat, ListadoCensal, ContribSolidaria, PoblacionsinSisben, \
PoblacionEspsinLS, SIAseguramiento, PlanCobertura, AfilOficioSinSisben, AfilSubGrupo5SinSisben, \
Movilidad, SegPortabilidad, Portabilidades, NovLcRegTipo1, NovLcRegTipo2, NovLcRegTipo3, \
NovLcRegTipo4, NovLcRegTipo5, NovLcRegTipo6, NovLcRegTipo7, NovLcRegTipo8, NovLcRegTipo9, \
NovLcRegTipo10, NovLcRegTipo11, NovLcRegTipo12

from cnf.models import Sexo, Departamento, Municipio, Area, Tipodoc, Eps, Etnia, ActividadEconomica, \
Ips, Institucion

from .forms import ImportFilemsForm, RepNovedadForm, ReportNodevadesForm, \
FormularioafilForm, SatForm, ListadoCensalForm, ContribucionSolidariaForm, ContribucionSolidariaForm, \
PoblacionEspsinLSForm, SIAseguramientoForm, PlanCoberturaForm, AfilOficioSinSisbenForm, \
AfilSubGrupo5SinSisbenForm, MovilidadForm, SegPortabilidadForm, PortabilidadForm, NovLcRegTipo1Form, \
NovLcRegTipo2Form, NovLcRegTipo2FormSet, NovLcRegTipo3FormSet, NovLcRegTipo4FormSet, \
NovLcRegTipo5FormSet, NovLcRegTipo6FormSet, NovLcRegTipo7FormSet, NovLcRegTipo8FormSet, \
NovLcRegTipo9FormSet, NovLcRegTipo10FormSet, NovLcRegTipo11FormSet, NovLcRegTipo12FormSet

# Create your views here.


class Principal(Sin_privilegio, generic.TemplateView):
	permission_required="aseg.view_Maestrosub"	
	template_name='base/basebdua.html'

def aseg_reload(request):
	context = {}
	registros = Maestrosub.objects.all()
	lista = list(registros.values("id","identificacion", "razonsocial", "fechanac", "eps__descripcion", \
		"fechaafiliacion", "estadoafil"))	
	context["datos"] = lista
	return JsonResponse(context, safe=False)
 
def dt_serverside(request):
	context = {}
	dt = request.GET 

	draw = int(dt.get("draw"))
	start = int(dt.get("start"))
	length = int(dt.get("length"))
	search = dt.get("search[value]")

	
	registros = Maestrosub.objects.all().values("id","identificacion","razonsocial","fechanac","eps__descripcion", \
		"fechaafiliacion", "estadoafil").order_by("id")
	if search:
		registros = registros.filter(
			Q(id__icontains=search) |
			Q(identificacion__icontains=search) |
			Q(razonsocial__icontains=search) |
			Q(eps__descripcion__icontains=search) |			
			Q(estadoafil__icontains=search)
			)
	
	recordsTotal = registros.count()
	recordsFiltered = recordsTotal
	#preparamos la salida
	context["draw"] = draw
	context["recordsTotal"] = recordsTotal
	context["recordsFiltered"] = recordsFiltered

	reg = registros[start:start + length]
	
	paginator = Paginator(reg, length)
	try:
		obj = paginator.page(draw).object_list
	except PageNotAnInteger:
		obj = paginator.page(draw).object_list
	except:
		obj = paginator.page(paginator.num_pages).object_list

	datos = [
		{		
		"id":d['id'],
		"identificacion":d['identificacion'],
		"razonsocial":d['razonsocial'],
		"fechanac":d['fechanac'],
		"eps__descripcion":d['eps__descripcion'],
		"fechaafiliacion":d['fechaafiliacion'],
		"estadoafil":d['estadoafil']
		} for d in obj
	]
	context["datos"] = datos 
	return JsonResponse(context,safe=False)

class MaestroListSS(Sin_privilegio, generic.TemplateView):
	permission_required="aseg.view_Maestrosub"	
	template_name='aseg/maestrobdua_list.html'

class MaestrobduaList(Sin_privilegio, generic.ListView):
	permission_required="aseg.view_Maestrosub"
	model=Maestrosub
	#paginate_by=100
	context_object_name = "obj"
	template_name='aseg/maestrobdua_list.html'
	#login_url = 'cnf:login'


class MaestrocontList(Sin_privilegio, generic.ListView):
	permission_required="aseg.view_maestrocont"
	model=Maestrocont
	#paginate_by=100
	context_object_name = "obj"
	template_name='aseg/maestrocontributivo_list.html'
	#login_url = 'cnf:login'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data= {}			
		action=request.POST.get("action", "searchdata")

		mc =Maestrocont.objects.all().values("id","identificacion","razonsocial","fechanac","eps__descripcion", \
			"fechaafiliacion","estadoactual")
				
		try:			
			if action == 'searchdata':
				data=[]
				for i in mc:
					data.append(i)				
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data[0] = str(e)			
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Listado de rediarios'
		context['create_url'] = reverse_lazy('pai:rediario_new')
		context['list_url'] = reverse_lazy('pai:rediario_list')
		context['entity'] = 'Maestrocont'
		return context

#inicio maestro contributivo server side
class ContributivoListSS(Sin_privilegio, generic.TemplateView):
	permission_required="aseg.view_maestrocont"	
	template_name='aseg/maestrocontributivo_list.html'

def aseg_reload_contributivo(request):
	context = {}
	registros = Maestrocont.objects.all()
	lista = list(registros.values("id","identificacion", "razonsocial", "fechanac", "eps__descripcion", \
		"fechaafiliacion", "estadoactual"))	
	context["datos"] = lista
	return JsonResponse(context, safe=False)

def dt_serverside_contributivo(request):
	context = {}
	dt = request.GET 

	draw = int(dt.get("draw"))
	start = int(dt.get("start"))
	length = int(dt.get("length"))
	search = dt.get("search[value]")

	registros = Maestrocont.objects.all().values("id","identificacion","razonsocial","fechanac","eps__descripcion", \
		"fechaafiliacion", "estadoactual").order_by("id")
	if search:
		registros = registros.filter(
			Q(id__icontains=search) |
			Q(identificacion__icontains=search) |
			Q(razonsocial__icontains=search) |
			Q(eps__descripcion__icontains=search) |			
			Q(estadoactual__icontains=search)
			)
	
	recordsTotal = registros.count()
	recordsFiltered = recordsTotal
	#preparamos la salida
	context["draw"] = draw
	context["recordsTotal"] = recordsTotal
	context["recordsFiltered"] = recordsFiltered

	reg = registros[start:start + length]
	
	paginator = Paginator(reg, length)
	try:
		obj = paginator.page(draw).object_list
	except PageNotAnInteger:
		obj = paginator.page(draw).object_list
	except:
		obj = paginator.page(paginator.num_pages).object_list
	
	datos = [
		{		
		"id":d['id'],
		"identificacion":d['identificacion'],
		"razonsocial":d['razonsocial'],
		"fechanac":d['fechanac'],
		"eps__descripcion":d['eps__descripcion'],
		"fechaafiliacion":d['fechaafiliacion'],
		"estadoactual":d['estadoactual']
		} for d in obj
	]
	context["datos"] = datos 
	return JsonResponse(context,safe=False)
# fin server side maestro contributivo


def importarmaestrocontributivo(request):
	form = ImportFilemsForm(request.POST or None, request.FILES or None)
	template='aseg/importmaestrocontributivo.html'	
	contexto = {'form':form} 	
	linea=[]
	if form.is_valid():
		form.save()
		form = ImportFilemsForm()
		obj = MaestrobduaCargado.objects.get(activated=False)
		mc = Maestrocont.objects.all().update(estado=False)
		with open(obj.file_name.path, 'rt') as url:
			df = pd.read_csv (url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')			
			#dfnew = df.fillna(value=0)
			nroreg = df.shape[0] #nro de  registros
			mc = Maestrocont.objects.all()
			mc.delete()
			loop = tqdm(nroreg, position=10, leave=False)
			for i, row in df.iterrows():				
				loop.set_description("loading... ".format(i))
				loop.update(i)
				eps = row[1]
				tbleps = Eps.objects.filter(codigo=eps).first()
				tipodoccotiza = row[2]
				tbltipodoccotiza = Tipodoc.objects.filter(codigo=tipodoccotiza).first()
				identificacioncotiza  =row[3]
				tipodoc = row[4] #Tipo documento del afiliado
				tbltipodoc = Tipodoc.objects.filter(codigo=tipodoc).first()
				identificacion  =row[5] #Nro del documento del afiliado
				apellido1 = row[6]
				apellido2 = row[7]
				if pd.isna(apellido2):
					apellido2 = ''
				nombre1 = row[8]
				nombre2 = row[9]
				if pd.isna(nombre2):
					nombre2 = ''
				fechanac = row[10]
				sexo = row[11]
				tblsexo= Sexo.objects.filter(codigo = sexo).first()
				if pd.isna(row[12]): #tipo de cotizante
					tipocotizante = ''
				else:
					tipocotizante = row[12] #Tipo de contizante				
				tbltipocotizante = Tipocontizante.objects.filter(codigo=tipocotizante).first()

				tipoafiliado = row[13] #Tipo de afiliado			
				tbltipoafiliado = Tipoafiliado.objects.filter(codigo=tipoafiliado).first()

				parentezcocf = row[14] #Parentezco				
				tblparentezco = Parentezcocf.objects.filter(codigo=parentezcocf).first()

				condiciondiscapacidad = row[15] #anteriormente D=Discapacitado E=Estudiante
				if pd.isna(condiciondiscapacidad):
					condiciondiscapacidad = ''
				tblconddiscapacidad = Condiciondiscapacidad.objects.filter(codigo=condiciondiscapacidad).first()
				
				#organizar en la entrada en vigencia de los nuevos algoritmos salto de dos campos

				departamento = row[18]
				tbldpto = Departamento.objects.filter(codigo=departamento).first()

				municipio = row[19]
				tblmunicipio = Municipio.objects.filter(codigo=municipio).first()

				area = row[20]
				tblarea = Area.objects.filter(codigo=area).first()

				fechaafiliacion = row[21]

				if pd.isna(row[23]): #Tipo documento del aportante
					tipodocaporta = 0
				else:
					tipodocaporta = row[23]

				tbltipodocaporta = Tipodoc.objects.filter(codigo=tipodocaporta).first()
				if pd.isna(row[24]):
					identificacionaporta =''
				else:
					identificacionaporta=row[24]


				if pd.isna(row[25]):
					actividadeconomica =''
				else:
					actividadeconomica=row[25]

				tblactividadeconomica = ActividadEconomica.objects.filter(codigo=actividadeconomica).first()

				if pd.isna(row[26]):
					ipsprimaria ='0'
				else:
					ipsprimaria=row[26]	
				tblipsprimaria = Ips.objects.filter(codhabilitacion=ipsprimaria).first()


				if pd.isna(row[27]):
					ipsodontologica ='0'
				else:
					ipsodontologica=row[27]	
				tblipsodontologica = Ips.objects.filter(codhabilitacion=ipsodontologica).first()

				estadoactual = row[28]

				#aseg = Maestrocont()
				#if not aseg:
				aseg = Maestrocont.objects.filter(tipodoc_id=tbltipodoc.pk).filter(identificacion=identificacion).first()
				if aseg:
					aseg.fechaafiliacion = datetime.strptime(fechaafiliacion, '%d/%m/%Y')
					aseg.eps = tbleps
					aseg.estado = True 
					aseg.save()
				else:
					aseg = Maestrocont()
					aseg.eps = tbleps
					if tbltipodoccotiza:
						aseg.tipodoccotizante = tbltipodoc
					aseg.identificacioncotiza = identificacion
					if tbltipodoc:
						aseg.tipodoc = tbltipodoc
					aseg.identificacion = identificacion
					aseg.apellido1 = apellido1
					aseg.apellido2 = apellido2
					aseg.nombre1 = nombre1
					aseg.nombre2 = nombre2
					fechanac = datetime.strptime(fechanac, '%d/%m/%Y')
					aseg.fechanac = fechanac
					if tblsexo:
						aseg.sexo = tblsexo

					if tbltipocotizante:
						aseg.tipocotizante = tbltipocotizante

					if tbltipoafiliado:
						aseg.tipoafiliado = tbltipoafiliado

					if tblconddiscapacidad:
						aseg.condiciondiscapacidad = tblconddiscapacidad

					if tblparentezco:
						aseg.parentezcocf = tblparentezco

					if tbldpto:
						aseg.departamento = tbldpto

					if tblmunicipio:
						aseg.municipio = tblmunicipio

					if tblarea:
						aseg.area = tblarea

					aseg.fechaafiliacion = datetime.strptime(fechaafiliacion, '%d/%m/%Y')

					if tbltipodocaporta:
						aseg.tipodocaporta = tbltipodocaporta

					aseg.identaportante = identificacionaporta

					if tblactividadeconomica:
						aseg.actividadeconomica = tblactividadeconomica

					if tblipsprimaria:
						aseg.ipsprimaria = tblipsprimaria

					if tblipsodontologica:
						aseg.ipsodontologica = tblipsodontologica

					aseg.estadoactual = estadoactual

					aseg.save()

			print("Termino de iterar")
			loop.close		

		obj.activated = True
		obj.save()
	
		return redirect('aseg:maestrocont_list')
	return render(request,template, contexto) 


def importarmaestrobdua(request):
	form = ImportFilemsForm(request.POST or None, request.FILES or None)
	template='aseg/importmaestrobdua.html'	
	contexto = {'form':form} 	
	linea=[]
	if form.is_valid():
		form.save()
		form = ImportFilemsForm()
		obj = MaestrobduaCargado.objects.get(activated=False)

		with open(obj.file_name.path, 'rt') as url:
			df = pd. read_csv (url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')			
			#dfnew = df.fillna(value=0)
			nroreg = df.shape[0]
			loop = tqdm(nroreg, position=10, leave=False)
			ms = Maestrosub.objects.all().update(estado=False)
			#ms.delete()
			for i, row in df.iterrows():				
				loop.set_description("loading... ".format(i))
				loop.update(i)
				eps = row[1]
				tbleps = Eps.objects.filter(codigo=eps).first()
				if not tbleps:
					strdato = "la Eps con código {} no existe".format(eps)
					raise ValidationError(strdato)
				tipodoc = row[4]
				tbltipodoc = Tipodoc.objects.filter(codigo=tipodoc).first()
				identificacion =row[5]
				apellido1 = row[6]
				apellido2 = row[7]
				if pd.isna(apellido2):
					apellido2 = ''
				nombre1 = row[8]
				nombre2 = row[9]
				if pd.isna(nombre2):
					nombre2 = ''
				fechanac = row[10]
				sexo = row[11]
				tblsexo= Sexo.objects.filter(codigo = sexo).first()

				departamento = row[18]
				tbldpto = Departamento.objects.filter(codigo=departamento).first()

				municipio = row[19]
				tblmunicipio = Municipio.objects.filter(codigo=municipio).first()

				area = row[20]
				tblarea = Area.objects.filter(codigo=area).first()

				fechaafiliacion = row[21]

				if pd.isna(row[14]):
					tipopoblacionesp = 0
				else:
					tipopoblacionesp = int(row[14]) #grupo poblacional

				tbltipopobesp = Tipopoblacionesp.objects.filter(codigo=tipopoblacionesp).first()
				
				nivelsisben = row[15]
				if pd.isna(nivelsisben):
					nivelsisben = ''
				tblnivsisben = Nivelsisben.objects.filter(codigo=nivelsisben).first()
				codigoipsprimaria = ''
				metodologiagp = ''
				tblmetodogp = Metodologiagp.objects.filter(codigo=metodologiagp).first()

				subgruposisbeniv = row[16]
				if pd.isna(subgruposisbeniv):
					subgruposisbeniv = ''
				condiciondiscapacidad = row[17] #anteriormente D=Discapacitado E=Estudiante
				tblconddiscapacidad = Condiciondiscapacidad.objects.filter(codigo=condiciondiscapacidad).first()

				if pd.isna(condiciondiscapacidad):
					condiciondiscapacidad = ''
				tipodoccabezafam = row[2]
				tbltdcabfam = Tipodoc.objects.filter(codigo=tipodoccabezafam).first()
				identificacioncabfam = row[3]
				parentezcocf = row[13]				
				if pd.isna(parentezcocf):
					parentezcocf = ''
				
				tblparentezco = Parentezcocf.objects.filter(codigo=parentezcocf).first()
				tipoafiliado = row[12]
				etnia = row[26]
				if pd.isna(etnia):
					etnia = ''
				else:
					if length(etnia) < 2:
						etnia = '0'+str(etnia)
				
				tbletnia = Etnia.objects.filter(codigo=etnia).first()

				resguardo = ''
				tblresguardo = Resguardo.objects.filter(codigo=resguardo).first()
				ipsodontologica = ''
				estadoafil = row[28]#usuario activo o inactivo 
				if  pd.isna(subgruposisbeniv):
					subgruposisbeniv = ''

				aseg = Maestrosub.objects.filter(tipodoc_id=tbltipodoc.pk).filter(identificacion=identificacion).first()
				if aseg:
					aseg.fechaafiliacion = datetime.strptime(fechaafiliacion, '%d/%m/%Y')
					aseg.eps = tbleps
					aseg.estado = True 
					aseg.save()
				else:
					aseg = Maestrosub()
					aseg.eps = tbleps
					if tbltipodoc:
						aseg.tipodoc = tbltipodoc
					aseg.identificacion = identificacion
					aseg.apellido1 = apellido1
					aseg.apellido2 = apellido2
					aseg.nombre1 = nombre1
					aseg.nombre2 = nombre2
					fechanac = datetime.strptime(fechanac, '%d/%m/%Y')
					aseg.fechanac = fechanac
					if tblsexo:
						aseg.sexo = tblsexo
					if tbldpto:
						aseg.departamento = tbldpto

					if tblmunicipio:
						aseg.municipio = tblmunicipio

					if tblarea:
						aseg.area = tblarea

					aseg.fechaafiliacion = datetime.strptime(fechaafiliacion, '%d/%m/%Y')
					if tbltipopobesp:
						aseg.tipopoblacionesp = tbltipopobesp

					if tblnivsisben:
						aseg.nivelsisben = tblnivsisben

					aseg.codigoipsprimaria = codigoipsprimaria
					if tblmetodogp:
						aseg.metodologiagp = tblmetodogp
					aseg.subgruposisbeniv = subgruposisbeniv
					
					if tblconddiscapacidad:
						aseg.condiciondiscapacidad = tblconddiscapacidad
					if tbltdcabfam:
						aseg.tipodoccabezafam = tbltdcabfam
					aseg.identificacioncabfam = identificacioncabfam
					if tblparentezco:
						aseg.parentezcocf = tblparentezco
					aseg.tipoafiliado = tipoafiliado
					
					if tbletnia:
						aseg.etnia = tbletnia

					if tblresguardo:
						aseg.resguardo = tblresguardo
					aseg.ipsodontologica = ipsodontologica
					aseg.estadoafil = estadoafil 
					aseg.save()

			print("Termino de iterar")
			loop.close		

		obj.activated = True
		obj.save()
	
		return redirect('aseg:maestrobdua_list')
	return render(request,template, contexto) 

class EstadisticaMS(generic.TemplateView):
	template_name='aseg/EstadisticaMS.html'

	def estadisticaxEAPB(self):
		diccionario = {}
		data=[]
		datosms = Maestrosub.objects.values('eps__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			nameps = x['eps__descripcion']
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				data.append(diccionario)
		return data

	def estadisticaxTipoPoblacion(self):
		diccionario = {}
		data=[]
		datosms = Maestrosub.objects.values('tipopoblacionesp__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			pobesp = x['tipopoblacionesp__descripcion']
			if pobesp == None:
				pobesp="Sin dato"

			if cant > 0:
				diccionario = {'name':pobesp,'y':cant}
				data.append(diccionario)
		return data

	def estadisticaSexo(self):
		diccionario = {}
		data=[]
		datosms = Maestrosub.objects.values('sexo__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			datoagrupacion = x['sexo__descripcion']
			if datoagrupacion == None:
				datoagrupacion="Sin dato"

			if cant > 0:
				diccionario = {'name':datoagrupacion,'y':cant}
				data.append(diccionario)
		return data


	def estadisticaArea(self):
		diccionario = {}
		data=[]
		datosms = Maestrosub.objects.values('area__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			datoagrupacion = x['area__descripcion']
			if datoagrupacion == None:
				datoagrupacion="Sin dato"

			if cant > 0:
				diccionario = {'name':datoagrupacion,'y':cant}
				data.append(diccionario)
		return data



	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['eps']= self.estadisticaxEAPB()
	    context['tipopob']= self.estadisticaxTipoPoblacion()
	    context['sexo']= self.estadisticaSexo()
	    context['area']= self.estadisticaArea()  
	        
	    return context



class EstadisticaMC(generic.TemplateView):
	template_name='aseg/EstadisticaMC.html'

	def estadisticaxEAPB(self):
		diccionario = {}
		data=[]
		datosms = Maestrocont.objects.values('eps__descripcion').annotate(cant=Count('id')).order_by('-cant')

		for x in datosms:
			cant = x['cant']
			nameps = x['eps__descripcion']
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				data.append(diccionario)
		return data

	
	def estadisticaSexo(self):
		diccionario = {}
		data=[]
		datosms = Maestrocont.objects.values('sexo__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			datoagrupacion = x['sexo__descripcion']
			if datoagrupacion == None:
				datoagrupacion="Sin dato"

			if cant > 0:
				diccionario = {'name':datoagrupacion,'y':cant}
				data.append(diccionario)
		return data


	def estadisticaArea(self):
		diccionario = {}
		data=[]
		datosms = Maestrocont.objects.values('area__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			datoagrupacion = x['area__descripcion']
			if datoagrupacion == None:
				datoagrupacion="Sin dato"

			if cant > 0:
				diccionario = {'name':datoagrupacion,'y':cant}
				data.append(diccionario)
		return data



	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['eps']= self.estadisticaxEAPB()
	    context['sexo']= self.estadisticaSexo()
	    context['area']= self.estadisticaArea()  	        
	    return context

class RepNovedadList(Sin_privilegio, generic.ListView):
	permission_required="aseg.view_repnovedad"
	model=RepNovedad
	context_object_name = "obj"
	template_name='aseg/repnovedad_list.html'
	login_url = 'cnf:login'

class RepNovedadCreate(Sin_privilegio, generic.CreateView):
	permission_required="aseg.add_repnovedad"
	model = RepNovedad
	template_name = 'aseg/repnovedad_form.html'
	context_object_name = 'obj'
	form_class = RepNovedadForm	
	success_url = reverse_lazy('aseg:reporte_novedad_list')	
	login_url = 'cnf:login'

class RepNovedadUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="aseg.change_repnovedad"
	model = RepNovedad
	template_name = 'aseg/repnovedad_form.html'
	context_object_name = 'obj'
	form_class = RepNovedadForm	
	success_url = reverse_lazy('aseg:reporte_novedad_list')	
	login_url = 'cnf:login'

class ReportNovedades(Sin_privilegio, generic.TemplateView):
	permission_required="aseg.view_repnovedad"
	template_name = 'aseg/reportenovedad_rep.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		data= {}
				
		try:			
			action=request.POST.get("action")
			if action == 'search_report':
				data=[]
				
				start_date=request.POST.get('start_date','')
				end_date=request.POST.get('end_date','')
				search =RepNovedad.objects.all().values("fecha","paciente__tipodoc__descripcion",\
					"paciente__identificacion","paciente__razonsocial","novedadbdua__codigo","fecininovedad")
				if len(start_date) and len(end_date):
					search = search.filter(fecha__range=[start_date, end_date])
				for s in search:
					data.append([
							s['fecha'].strftime('%Y-%m-%d'),
							s['paciente__tipodoc__descripcion'],							
							s['paciente__identificacion'],
							s['paciente__razonsocial'],
							s['novedadbdua__codigo'],
							s['fecininovedad'].strftime('%Y-%m-%d')
						])

							
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data[0] = str(e)			
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		context['list_url']= reverse_lazy('aseg:novedad_report')
		context['titulo']= 'Generar reporte de novedades'		
		context['form']=ReportNodevadesForm()
		return context

@method_decorator(csrf_exempt)
def report_novedad_csv_view(request, fec_ini, fec_fin):
	institucion=Institucion.objects.filter(pk=1).first()
	fecha_dt = datetime.strptime(fec_fin, '%Y-%m-%d')
	anio=fecha_dt.year
	anio=str(anio)
	mes=fecha_dt.month
	if mes<10:
		mes='0'+str(mes)
	else:
		mes=str(mes)

	dia=fecha_dt.day
	if dia<10:
		dia='0'+str(dia)
	else:
		dia=str(dia)


	filename='NS'+institucion.departamento.codigo+institucion.municipio.codigo+dia+mes+anio+'.txt'
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="'+filename+'"'},
        )
	writer = csv.writer(response)

	data= {}
	action='export_report'


	print(action)	
	if action == 'export_report':
		data=[]
		start_date= fec_ini
		end_date= fec_fin

		search =RepNovedad.objects.all().values("fecha","paciente__tipodoc__codigo",\
			"eps__codigo","departamento__codigo","municipio__codigo","paciente__fechanac",\
			"paciente__identificacion","paciente__nombre1","paciente__nombre2","paciente__apellido1",\
			"paciente__apellido2","novedadbdua__codigo","fecininovedad", "valor1", "valor2", \
			"valor3","valor4","valor5", "valor6", "valor7")
		if len(start_date) and len(end_date):
			search = search.filter(fecha__range=[start_date, end_date])
		k=1
		for s in search:
			data.append([
				k,
				s['eps__codigo'],
				s['paciente__tipodoc__codigo'],							
				s['paciente__identificacion'],
				s['paciente__apellido1'],
				s['paciente__apellido2'],
				s['paciente__nombre1'],
				s['paciente__nombre2'],
				s['paciente__fechanac'].strftime('%d/%m/%Y'),
				s['departamento__codigo'],
				s['municipio__codigo'],
				s['novedadbdua__codigo'],
				s['fecininovedad'].strftime('%d/%m/%Y'),
				s['valor1'],
				s['valor2'],
				s['valor3'],
				s['valor4'],
				s['valor5'],
				s['valor6'],
				s['valor7']
				])
			k = k+1

		for d in data:
			writer.writerow(d)
	
		print(writer)
	return response


class FormularioafilList(Sin_privilegio, generic.ListView):
	permission_required="aseg.view_formularioafil"
	model=Formularioafil
	context_object_name = "obj"
	template_name='aseg/formulario_afiliacion_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Gestionar formularios de Afiliación'				
		return context

class FormularioafilCreate(Sin_privilegio, generic.CreateView):
	permission_required="aseg.add_formularioafil"
	model = Formularioafil
	template_name = 'aseg/formulario_afiliacion_form.html'
	context_object_name = 'obj'
	form_class = FormularioafilForm	
	success_url = reverse_lazy('aseg:fua_list')	
	login_url = 'cnf:login'

class FormularioafilUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="aseg.change_formularioafil"
	model = Formularioafil
	template_name = 'aseg/formulario_afiliacion_form.html'
	context_object_name = 'obj'
	form_class = FormularioafilForm	
	success_url = reverse_lazy('aseg:fua_list')	
	login_url = 'cnf:login'



class SatList(Sin_privilegio, generic.ListView):
	permission_required="aseg.view_sat"
	model=Sat
	context_object_name = "obj"
	template_name='aseg/sat_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Gestionar sistema de afiliación transaccional'				
		return context

class SatCreate(Sin_privilegio, generic.CreateView):
	permission_required="aseg.add_sat"
	model = Sat
	template_name = 'aseg/sat_form.html'
	context_object_name = 'obj'
	form_class = SatForm	
	success_url = reverse_lazy('aseg:sat_list')	
	login_url = 'cnf:login'

class SatUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="aseg.change_sat"
	model = Sat
	template_name = 'aseg/sat_form.html'
	context_object_name = 'obj'
	form_class = SatForm	
	success_url = reverse_lazy('aseg:sat_list')	
	login_url = 'cnf:login'



class ListadoCensaList(Sin_privilegio, generic.ListView):
	permission_required="view_listadocensal"
	model=ListadoCensal
	context_object_name = "obj"
	template_name='aseg/listado_censal_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Gestionar listados censales'				
		return context

class ListadoCensalCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_listadocensal"
	model = ListadoCensal
	template_name = 'aseg/listado_censal_form.html'
	context_object_name = 'obj'
	form_class = ListadoCensalForm	
	success_url = reverse_lazy('aseg:list_censal_list')	
	login_url = 'cnf:login'

class ListadoCensalUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_listadocensal"
	model = ListadoCensal
	template_name = 'aseg/listado_censal_form.html'
	context_object_name = 'obj'
	form_class = ListadoCensalForm	
	success_url = reverse_lazy('aseg:list_censal_list')	
	login_url = 'cnf:login'


class ContribSolidariaList(Sin_privilegio, generic.ListView):
	permission_required="view_contribsolidaria"
	model=ContribSolidaria
	context_object_name = "obj"
	template_name='aseg/contrib_solidaria_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Gestionar Contribución solidaria'				
		return context

class ContribSolidariaCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_contribsolidaria"
	model = ContribSolidaria
	template_name = 'aseg/contrib_solidaria_form.html'
	context_object_name = 'obj'
	form_class = ContribucionSolidariaForm	
	success_url = reverse_lazy('aseg:contr_solidaria_list')	
	login_url = 'cnf:login'

class ContribSolidariaUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_contribsolidaria"
	model = ContribSolidaria
	template_name = 'aseg/contrib_solidaria_form.html'
	context_object_name = 'obj'
	form_class = ContribucionSolidariaForm	
	success_url = reverse_lazy('aseg:contr_solidaria_list')	
	login_url = 'cnf:login'

class PobSinSisbenList(Sin_privilegio, generic.ListView):
	permission_required="view_poblacionsinsisben"
	model=PoblacionsinSisben
	context_object_name = "obj"
	template_name='aseg/pob_sin_encuesta_sisben_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Seguimiento a población sin encuesta sisbén'				
		return context

class PobSinSisbenCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_poblacionsinsisben"
	model = PoblacionsinSisben
	template_name = 'aseg/pob_sin_encuesta_sisben_form.html'
	context_object_name = 'obj'
	form_class = ContribucionSolidariaForm	
	success_url = reverse_lazy('aseg:pob_sin_sisben_list')	
	login_url = 'cnf:login'

class PobSinSisbenUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_poblacionsinsisben"
	model = PoblacionsinSisben
	template_name = 'aseg/pob_sin_encuesta_sisben_form.html'
	context_object_name = 'obj'
	form_class = ContribucionSolidariaForm	
	success_url = reverse_lazy('aseg:pob_sin_sisben_list')	
	login_url = 'cnf:login'


class PoblacionEspsinLSList(Sin_privilegio, generic.ListView):
	permission_required="view_poblacionespsinls"
	model=PoblacionEspsinLS
	context_object_name = "obj"
	template_name='aseg/pob_esp_sin_lc_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Seguimiento a población especial sin listado censal'				
		return context

class PoblacionEspsinLSCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_poblacionespsinls"
	model = PoblacionEspsinLS
	template_name = 'aseg/pob_esp_sin_lc_form.html'
	context_object_name = 'obj'
	form_class = PoblacionEspsinLSForm	
	success_url = reverse_lazy('aseg:pobespsinlc_list')	
	login_url = 'cnf:login'

class PoblacionEspsinLSUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_poblacionespsinls"
	model = PoblacionEspsinLS
	template_name = 'aseg/pob_esp_sin_lc_form.html'
	context_object_name = 'obj'
	form_class = PoblacionEspsinLSForm	
	success_url = reverse_lazy('aseg:pobespsinlc_list')	
	login_url = 'cnf:login'


class SIAseguramientoList(Sin_privilegio, generic.ListView):
	permission_required="view_poblacionespsinls"
	model=SIAseguramiento
	context_object_name = "obj"
	template_name='aseg/si_utilizado_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Sistema de información utilizado'				
		return context

class SIAseguramientoCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_poblacionespsinls"
	model = SIAseguramiento
	template_name = 'aseg/si_utilizado_form.html'
	context_object_name = 'obj'
	form_class = SIAseguramientoForm	
	success_url = reverse_lazy('aseg:siutilizado_list')	
	login_url = 'cnf:login'

class SIAseguramientoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_poblacionespsinls"
	model = SIAseguramiento
	template_name = 'aseg/si_utilizado_form.html'
	context_object_name = 'obj'
	form_class = SIAseguramientoForm	
	success_url = reverse_lazy('aseg:siutilizado_list')	
	login_url = 'cnf:login'


class PlanCoberturaList(Sin_privilegio, generic.ListView):
	permission_required="view_plancobertura"
	model=PlanCobertura
	context_object_name = "obj"
	template_name='aseg/plan_cobertura_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Plan de cobertura'				
		return context

class PlanCoberturaCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_plancobertura"
	model = PlanCobertura
	template_name = 'aseg/plan_cobertura_form.html'
	context_object_name = 'obj'
	form_class = PlanCoberturaForm	
	success_url = reverse_lazy('aseg:plan_cobertura_list')	
	login_url = 'cnf:login'

class PlanCoberturaUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_plancobertura"
	model = PlanCobertura
	template_name = 'aseg/plan_cobertura_form.html'
	context_object_name = 'obj'
	form_class = PlanCoberturaForm	
	success_url = reverse_lazy('aseg:plan_cobertura_list')	
	login_url = 'cnf:login'

class AfilOficioSinSisbenList(Sin_privilegio, generic.ListView):
	permission_required="view_afiloficiosinsisben"
	model=AfilOficioSinSisben
	context_object_name = "obj"
	template_name='aseg/afil_oficio_sin_sisben_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Afiliado de oficio sin encuesta sisben IV'				
		return context

class AfilOficioSinSisbenCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_afiloficiosinsisben"
	model = AfilOficioSinSisben
	template_name = 'aseg/afil_oficio_sin_sisben_form.html'
	context_object_name = 'obj'
	form_class = AfilOficioSinSisbenForm	
	success_url = reverse_lazy('aseg:Afil_ofi_sin_sisben_list')	
	login_url = 'cnf:login'

class AfilOficioSinSisbenUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_afiloficiosinsisben"
	model = AfilOficioSinSisben
	template_name = 'aseg/afil_oficio_sin_sisben_form.html'
	context_object_name = 'obj'
	form_class = AfilOficioSinSisbenForm	
	success_url = reverse_lazy('aseg:Afil_ofi_sin_sisben_list')	
	login_url = 'cnf:login'


class AfilSubGrupo5SinSisbenList(Sin_privilegio, generic.ListView):
	permission_required="view_afilsubgrupo5sinsisben"
	model=AfilSubGrupo5SinSisben
	context_object_name = "obj"
	template_name='aseg/afil_sub_grupo5_sin_sisben_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Afiliado subsidiado grupo 5 sin encuesta Sisben IV'				
		return context

class AfilSubGrupo5SinSisbenCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_afilsubgrupo5sinsisben"
	model = AfilSubGrupo5SinSisben
	template_name = 'aseg/afil_sub_grupo5_sin_sisben_form.html'
	context_object_name = 'obj'
	form_class = AfilSubGrupo5SinSisbenForm	
	success_url = reverse_lazy('aseg:afil_sub_g5_sin_sisben_list')	
	login_url = 'cnf:login'

class AfilSubGrupo5SinSisbenUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_afilsubgrupo5sinsisben"
	model = AfilSubGrupo5SinSisben
	template_name = 'aseg/afil_sub_grupo5_sin_sisben_form.html'
	context_object_name = 'obj'
	form_class = AfilSubGrupo5SinSisbenForm	
	success_url = reverse_lazy('aseg:afil_sub_g5_sin_sisben_list')	
	login_url = 'cnf:login'


class MovilidadList(Sin_privilegio, generic.ListView):
	permission_required="view_movilidad"
	model=Movilidad
	context_object_name = "obj"
	template_name='aseg/movilidad_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Seguimiento Solicitud de Movilidad'				
		return context

class MovilidadCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_movilidad"
	model = Movilidad
	template_name = 'aseg/movilidad_form.html'
	context_object_name = 'obj'
	form_class = MovilidadForm	
	success_url = reverse_lazy('aseg:movilidad_list')	
	login_url = 'cnf:login'

class MovilidadUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_movilidad"
	model = Movilidad
	template_name = 'aseg/movilidad_form.html'
	context_object_name = 'obj'
	form_class = MovilidadForm	
	success_url = reverse_lazy('aseg:movilidad_list')	
	login_url = 'cnf:login'


class SegPortabilidadList(Sin_privilegio, generic.ListView):
	permission_required="view_segportabilidad"
	model=SegPortabilidad
	context_object_name = "obj"
	template_name='aseg/segportabilidad_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Seguimiento Solicitud de Portabilidad'				
		return context

class SegPortabilidadCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_segportabilidad"
	model = SegPortabilidad
	template_name = 'aseg/segportabilidad_form.html'
	context_object_name = 'obj'
	form_class = SegPortabilidadForm	
	success_url = reverse_lazy('aseg:seg_portabilidad_list')	
	login_url = 'cnf:login'

class SegPortabilidadUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_segportabilidad"
	model = SegPortabilidad
	template_name = 'aseg/segportabilidad_form.html'
	context_object_name = 'obj'
	form_class = SegPortabilidadForm	
	success_url = reverse_lazy('aseg:seg_portabilidad_list')	
	login_url = 'cnf:login'

class PortabilidadList(Sin_privilegio, generic.ListView):
	permission_required="view_portabilidades"
	model=Portabilidades
	context_object_name = "obj"
	template_name='aseg/portabilidad_list.html'
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Gestionar Portabilidad'				
		return context

class PortabilidadCreate(Sin_privilegio, generic.CreateView):
	permission_required="add_portabilidades"
	model = Portabilidades
	template_name = 'aseg/portabilidad_form.html'
	context_object_name = 'obj'
	form_class = PortabilidadForm	
	success_url = reverse_lazy('aseg:portabilidad_list')	
	login_url = 'cnf:login'

class PortabilidadUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="change_portabilidades"
	model = Portabilidades
	template_name = 'aseg/portabilidad_form.html'
	context_object_name = 'obj'
	form_class = PortabilidadForm	
	success_url = reverse_lazy('aseg:portabilidad_list')	
	login_url = 'cnf:login'


class NovLcRegTipo1List(Sin_privilegio, generic.ListView):
	permission_required="view_novlcregtipo1"	
	model = NovLcRegTipo1
	template_name='aseg/novlcregtipo1_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)				
		context['titulo']= 'Gestionar novedades listado censal'				
		return context

class NovLcInline():
	form_class = NovLcRegTipo1Form	
	model = NovLcRegTipo1
	template_name = 'aseg/novlcregtipo1_form.html'

	def obtener_total_registro(self, pk):
		dato = 0
		totreg2 = NovLcRegTipo2.objects.filter(novlcregtipo1_id=pk).count() 
		totreg3 = NovLcRegTipo3.objects.filter(novlcregtipo1_id=pk).count() 
		totreg4 = NovLcRegTipo4.objects.filter(novlcregtipo1_id=pk).count() 
		totreg5 = NovLcRegTipo5.objects.filter(novlcregtipo1_id=pk).count() 
		totreg6 = NovLcRegTipo6.objects.filter(novlcregtipo1_id=pk).count() 
		totreg7 = NovLcRegTipo7.objects.filter(novlcregtipo1_id=pk).count() 
		totreg8 = NovLcRegTipo8.objects.filter(novlcregtipo1_id=pk).count() 
		totreg9 = NovLcRegTipo9.objects.filter(novlcregtipo1_id=pk).count() 
		totreg10 = NovLcRegTipo10.objects.filter(novlcregtipo1_id=pk).count() 
		totreg11 = NovLcRegTipo11.objects.filter(novlcregtipo1_id=pk).count() 
		totreg12 = NovLcRegTipo12.objects.filter(novlcregtipo1_id=pk).count() 

		dato = totreg2 + totreg3 + totreg4 + totreg5 + totreg6 +totreg7 +totreg8 +totreg9 +totreg10 +totreg11 +totreg12
		return dato

	def form_valid(self, form):		
		named_formsets = self.get_named_formsets()
		if not all((x.is_valid() for x in named_formsets.values())):
			return self.render_to_response(self.get_context_data(form=form))

		self.object = form.save()

		for name, formset in named_formsets.items():
			formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
			if formset_save_func is not None:				
				formset_save_func(formset)
			else:
				formset.save()

		#Actualizar la cantidad de registros cargados
		cantreg=0
		cantreg = self.obtener_total_registro(self.object.pk)		
		self.object.nrototalreg = cantreg
		self.object.save()
		return redirect('aseg:novlcregtipo1_list')

	
	def formset_novlcregtipo2_valid(self, formset):		
		novlcregt2 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt2:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo3_valid(self, formset):		
		novlcregt3 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt3:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo4_valid(self, formset):		
		novlcregt4 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt4:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo5_valid(self, formset):		
		novlcregt5 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt5:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo6_valid(self, formset):		
		novlcregt6 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt6:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo7_valid(self, formset):		
		novlcregt7 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt7:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo8_valid(self, formset):		
		novlcregt8 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt8:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo9_valid(self, formset):		
		novlcregt9 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt9:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo10_valid(self, formset):		
		novlcregt10 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt10:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo11_valid(self, formset):		
		novlcregt11 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt11:
			seg.novlcregtipo1 = self.object
			seg.save()

	def formset_novlcregtipo12_valid(self, formset):		
		novlcregt12 = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in novlcregt12:
			seg.novlcregtipo1 = self.object
			seg.save()


class NovLcRegTipo1Create(Sin_privilegio, NovLcInline, generic.CreateView):
	permission_required="add_novlcregtipo1"
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		ctx = super(NovLcRegTipo1Create, self).get_context_data(**kwargs)
		ctx['named_formsets'] = self.get_named_formsets()
		return ctx

	def get_named_formsets(self):
		if self.request.method == "GET":
			return {
                'novlcregtipo2': NovLcRegTipo2FormSet(prefix='novlcregtipo2'),
                'novlcregtipo3': NovLcRegTipo3FormSet(prefix='novlcregtipo3'),
                'novlcregtipo4': NovLcRegTipo4FormSet(prefix='novlcregtipo4'),
                'novlcregtipo5': NovLcRegTipo5FormSet(prefix='novlcregtipo5'),
                'novlcregtipo6': NovLcRegTipo6FormSet(prefix='novlcregtipo6'),
                'novlcregtipo7': NovLcRegTipo7FormSet(prefix='novlcregtipo7'),
                'novlcregtipo8': NovLcRegTipo8FormSet(prefix='novlcregtipo8'),
                'novlcregtipo9': NovLcRegTipo9FormSet(prefix='novlcregtipo9'),
                'novlcregtipo10': NovLcRegTipo10FormSet(prefix='novlcregtipo10'),
                'novlcregtipo11': NovLcRegTipo11FormSet(prefix='novlcregtipo11'),
                'novlcregtipo12': NovLcRegTipo12FormSet(prefix='novlcregtipo12'),
			}
		else:
			return {
                'novlcregtipo2': NovLcRegTipo2FormSet(self.request.POST or None, prefix='novlcregtipo2'),
                'novlcregtipo3': NovLcRegTipo3FormSet(self.request.POST or None, prefix='novlcregtipo3'),
                'novlcregtipo4': NovLcRegTipo4FormSet(self.request.POST or None, prefix='novlcregtipo4'),
                'novlcregtipo5': NovLcRegTipo5FormSet(self.request.POST or None, prefix='novlcregtipo5'),
                'novlcregtipo6': NovLcRegTipo6FormSet(self.request.POST or None, prefix='novlcregtipo6'),
                'novlcregtipo7': NovLcRegTipo7FormSet(self.request.POST or None, prefix='novlcregtipo7'),
                'novlcregtipo8': NovLcRegTipo8FormSet(self.request.POST or None, prefix='novlcregtipo8'),
                'novlcregtipo9': NovLcRegTipo9FormSet(self.request.POST or None, prefix='novlcregtipo9'),
                'novlcregtipo10': NovLcRegTipo10FormSet(self.request.POST or None, prefix='novlcregtipo10'),
                'novlcregtipo11': NovLcRegTipo11FormSet(self.request.POST or None, prefix='novlcregtipo11'),
                'novlcregtipo12': NovLcRegTipo12FormSet(self.request.POST or None, prefix='novlcregtipo12'),


            }

class NovLcRegTipo1Update(Sin_privilegio, NovLcInline, generic.UpdateView):
	permission_required="change_novlcregtipo1"
	#context_object_name = 'obj'
	#success_url = reverse_lazy('pqrs:pqrs_list')		
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		ctx = super(NovLcRegTipo1Update, self).get_context_data(**kwargs)
		ctx['named_formsets'] = self.get_named_formsets()
		ctx['obj']=self.object
		return ctx
	
	def get_named_formsets(self):
		return {
		'novlcregtipo2': NovLcRegTipo2FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo2'),
		'novlcregtipo3': NovLcRegTipo3FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo3'),
		'novlcregtipo4': NovLcRegTipo4FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo4'),
		'novlcregtipo5': NovLcRegTipo5FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo5'),
		'novlcregtipo6': NovLcRegTipo6FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo6'),
		'novlcregtipo7': NovLcRegTipo7FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo7'),
		'novlcregtipo8': NovLcRegTipo8FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo8'),
		'novlcregtipo9': NovLcRegTipo9FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo9'),
		'novlcregtipo10': NovLcRegTipo10FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo10'),
		'novlcregtipo11': NovLcRegTipo11FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo11'),
		'novlcregtipo12': NovLcRegTipo12FormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='novlcregtipo12'),

		}	

def delete_novlcregtipo2(request, pk):
	try:
		novlcregt2 = NovLcRegTipo2.objects.get(id=pk)
		novlcinline = NovLcInline()
		idregtipo1 = novlcregt2.novlcregtipo1.id
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=idregtipo1)		

	except NovLcRegTipo2.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 2 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=novlcregt2.novlcregtipo1.id)

	novlcregt2.delete()
	totreg = novlcinline.obtener_total_registro(idregtipo1)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()

	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=novlcregt2.novlcregtipo1.id)


def delete_novlcregtipo3(request, pk):
	try:
		novlcregt3 = NovLcRegTipo3.objects.get(id=pk)
		novlcinline = NovLcInline()
		idregtipo1 = novlcregt3.novlcregtipo1.id
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=idregtipo1)		


	except NovLcRegTipo3.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 3 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=novlcregt3.novlcregtipo1.id)

	novlcregt3.delete()
	totreg = novlcinline.obtener_total_registro(idregtipo1)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=novlcregt3.novlcregtipo1.id)

def delete_novlcregtipo4(request, pk):
	try:
		novlcregt4 = NovLcRegTipo4.objects.get(id=pk)
		newpk = novlcregt4.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)	

	except NovLcRegTipo4.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 4 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt4.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)

def delete_novlcregtipo5(request, pk):
	try:
		novlcregt5 = NovLcRegTipo5.objects.get(id=pk)
		newpk = novlcregt5.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)
		
	except NovLcRegTipo5.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 5 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt5.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)


def delete_novlcregtipo6(request, pk):
	try:
		novlcregt6 = NovLcRegTipo6.objects.get(id=pk)
		newpk = novlcregt6.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)
	except NovLcRegTipo6.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 6 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt6.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)


def delete_novlcregtipo7(request, pk):
	try:
		novlcregt7 = NovLcRegTipo7.objects.get(id=pk)
		newpk = novlcregt7.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)
		

	except NovLcRegTipo7.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 7 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt7.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)

def delete_novlcregtipo8(request, pk):
	try:
		novlcregt8 = NovLcRegTipo8.objects.get(id=pk)
		newpk = novlcregt8.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)

	except NovLcRegTipo8.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 8 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt8.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)


def delete_novlcregtipo9(request, pk):
	try:
		novlcregt9 = NovLcRegTipo9.objects.get(id=pk)
		newpk = novlcregt9.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)

	except NovLcRegTipo9.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 9 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt9.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)

def delete_novlcregtipo10(request, pk):
	try:
		novlcregt10 = NovLcRegTipo10.objects.get(id=pk)
		newpk = novlcregt10.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)

	except NovLcRegTipo10.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 10 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt10.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)


def delete_novlcregtipo11(request, pk):
	try:
		novlcregt11 = NovLcRegTipo11.objects.get(id=pk)
		newpk = novlcregt11.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)

	except NovLcRegTipo11.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 11 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt11.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)


def delete_novlcregtipo12(request, pk):
	try:
		
		novlcregt12 = NovLcRegTipo12.objects.get(id=pk)
		newpk = novlcregt12.novlcregtipo1.id
		novlcinline = NovLcInline()		
		novlctegtipo1 = NovLcRegTipo1.objects.get(id=newpk)

	except NovLcRegTipo12.DoesNotExist:
		messages.success(
			request, 'Novedad listado censal Reg tipo 12 no existe'
			)
		return redirect('aseg:novlcregtipo1_edit', pk=newpk)

	novlcregt12.delete()
	totreg = novlcinline.obtener_total_registro(newpk)
	novlctegtipo1.nrototalreg = totreg
	novlctegtipo1.save()
	messages.success(
		request, 'Novedad listado censal Eliminado satisfactoriamente'
		)
	return redirect('aseg:novlcregtipo1_edit', pk=newpk)


@method_decorator(csrf_exempt)
def report_novedadlc_csv_view(request, id):
	novlcregtipo1 = NovLcRegTipo1.objects.filter(pk=id).first()
	fecha_dt = novlcregtipo1.fechafinal

	anio=fecha_dt.year
	anio=str(anio)
	mes=fecha_dt.month
	if mes<10:
		mes='0'+str(mes)
	else:
		mes=str(mes)

	dia=fecha_dt.day
	if dia<10:
		dia='0'+str(dia)
	else:
		dia=str(dia)


	filename='REC125NLCE'+anio+mes+dia+novlcregtipo1.tipoentidad+novlcregtipo1.nroidententidad+'.txt'
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="'+filename+'"'},        
        )
	writer = csv.writer(response,delimiter='|')

	data= {}
	action='export_report'


	print(action)	
	if action == 'export_report':
		data=[]
		k=1
		#reg type 1
		data.append([
			novlcregtipo1.tiporegistro,			
			novlcregtipo1.tipoentidad,
			novlcregtipo1.nroidententidad,
			novlcregtipo1.fechafinal.strftime('%Y-%m-%d'),
			novlcregtipo1.nrototalreg
			])

		#end reg type 1


		#Registro tipo 2
		novlcreg =NovLcRegTipo2.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","tipodocnew__codigo","identificacionnew","causactdocumento__codigo",\
			"fechaaplicanovedad")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['tipodocnew__codigo'],
				s['identificacionnew'],
				s['causactdocumento__codigo'],
				s['fechaaplicanovedad'].strftime('%Y-%m-%d')				
				])
			k = k+1
		# end reg type 2

		#Registro tipo 3
		novlcreg =NovLcRegTipo3.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","nombre1new","nombre2new")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['nombre1new'],
				s['nombre2new']		
				])
			k = k+1
		# end reg type 3

		#Registro tipo 4
		novlcreg =NovLcRegTipo4.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","apellido1new","apellido2new")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['apellido1new'],
				s['apellido2new']		
				])
			k = k+1
		# end reg type 4

		#Registro tipo 5
		novlcreg =NovLcRegTipo5.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","municipio__codigo","municipio__departamento__codigo")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['municipio__departamento__codigo']+s['municipio__codigo']						
				])
			k = k+1
		# end reg type 5

		#Registro tipo 6
		novlcreg =NovLcRegTipo6.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","tipopoblacionesp__codigo","estadolc__codigo")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['tipopoblacionesp__codigo'],
				s['estadolc__codigo']		
				])
			k = k+1
		# end reg type 6

		#Registro tipo 7
		novlcreg =NovLcRegTipo7.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","sexo__codigo")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['sexo__codigo']
				])
			k = k+1
		# end reg type 7

		#Registro tipo 8
		novlcreg =NovLcRegTipo8.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","fechanac")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['fechanac'].strftime('%Y-%m-%d')	
				])
			k = k+1
		# end reg type 8

		#Registro tipo 9
		novlcreg =NovLcRegTipo9.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","tipopoblacionesp__codigo","tipobelegiblesub__codigo")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['tipopoblacionesp__codigo'],
				s['tipobelegiblesub__codigo']
				])
			k = k+1
		# end reg type 9

		#Registro tipo 10
		novlcreg =NovLcRegTipo10.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","tipopoblacionesp__codigo","tipopoblacionespnew__codigo")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['tipopoblacionesp__codigo'],
				s['tipopoblacionespnew__codigo']
				])
			k = k+1
		# end reg type 10

		#Registro tipo 11
		novlcreg =NovLcRegTipo11.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","tipodoctitular__codigo","identificaciontitular")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['tipodoctitular__codigo'],
				s['identificaciontitular']
				])
			k = k+1
		# end reg type 11

		#Registro tipo 12
		novlcreg =NovLcRegTipo12.objects.all().values("tiporegistro","tipodoc__codigo",\
			"identificacion","tipopoblacionesp__codigo")
		search = novlcreg.filter(novlcregtipo1=id)
		
		for s in search:
			data.append([
				s['tiporegistro'],
				k,
				s['tipodoc__codigo'],							
				s['identificacion'],
				s['tipopoblacionesp__codigo']				
				])
			k = k+1
		# end reg type 12
		for d in data:
			writer.writerow(d)
	
		print(writer)
	return response
