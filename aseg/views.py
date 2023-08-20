from django.views import generic
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pandas as pd
from datetime import datetime
from tqdm import tqdm

from cnf.views import Sin_privilegio
from .models import Maestrosub, MaestrobduaCargado, Tipopoblacionesp, Metodologiagp, Parentezcocf, \
Nivelsisben, Metodologiagp, Condiciondiscapacidad, Resguardo, Maestrocont, Tipocontizante, \
Tipoafiliado

from cnf.models import Sexo, Departamento, Municipio, Area, Tipodoc, Eps, Etnia, ActividadEconomica, \
Ips

from .forms import ImportFilemsForm

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
				tipodoc = row[4]
				tbltipodoc = Tipodoc.objects.filter(codigo=tipodoc).first()
				identificacion  =row[5]
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
				if pd.isna(row[12]):
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
			ms = Maestrosub.objects.all()
			ms.delete()
			for i, row in df.iterrows():				
				loop.set_description("loading... ".format(i))
				loop.update(i)
				eps = row[1]
				tbleps = Eps.objects.filter(codigo=eps).first()
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
				
				tbletnia = Etnia.objects.filter(codigo=etnia).first()

				resguardo = ''
				tblresguardo = Resguardo.objects.filter(codigo=resguardo).first()
				ipsodontologica = ''
				estadoafil = row[28]#usuario activo o inactivo 
				if  pd.isna(subgruposisbeniv):
					subgruposisbeniv = ''

				#aseg = Maestrosub.objects.filter(tipodoc_id=tbltipodoc.pk).filter(identificacion=identificacion)

				#if not aseg:
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



