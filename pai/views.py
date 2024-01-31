from django.views import generic
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
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

from .models import VacunaCovid, RediarioCargado, Rediario, RediarioPaiRegCargado, \
      Rediarioregular, Biologico, Dosisbiologico, RediarioRegBiologico, Jeringas

from cnf.models import Tipodoc, Paciente, Barrio, Pais, Departamento, Municipio, Barrio, \
     Area, Regimen, Eps, Sexo, Etnia, Ips

from aseg.models import Maestrosub, Maestrocont 

from .forms import ImportFileForm, RediarioCreateForm, ImportFilePaiRegForm
from cnf.views import Sin_privilegio



# Create your views here.


class PrincipalPai(Sin_privilegio, generic.TemplateView):
	permission_required="pai.view_VacunaCovid"	
	template_name='base/basepai.html'

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

def insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos):
	
	redreg = RediarioRegBiologico.objects.filter(rediarioregular=red).filter(biologico=tblbiol).first()
	if not redreg:

		if jeringa:
			jeringa = jeringa
		if tblbiol:
			tbldosisbiol = Dosisbiologico.objects.filter(biologico=tblbiol).filter(descripcion=dosisbiol).first()
				
		tbljeringa = Jeringas.objects.filter(descripcion=jeringa).first()
		redreg = RediarioRegBiologico()
		if tblbiol:
			redreg.biologico = tblbiol
		redreg.rediarioregular = red
		redreg.nrofrascos = nrofrascos
		if tbldosisbiol:
			redreg.dosisbiologico = tbldosisbiol
		redreg.loteBiologico = lotebiol
		if tbljeringa:
			redreg.jeringa = tbljeringa
			redreg.lotejeringa = lotejeringa
		if lotediluyente != None:
			redreg.lotediluyente = lotediluyente		
		redreg.save()

		return 'OK'
	return 'NR'


def importarRediariosPaiRegular(request):
	form = ImportFilePaiRegForm(request.POST or None, request.FILES or None)
	template='pai/importrediariospaireg.html'	
	contexto = {'form':form} 	
	linea=[]
	pacobj =[]
	idips = request.POST.get('ips')
	print("POST: ", request.POST)
	btlips = Ips.objects.filter(pk=idips).first()	
	if form.is_valid():
		form.save()
		form = ImportFilePaiRegForm()
		obj = RediarioPaiRegCargado.objects.get(activated=False)
		with open(obj.file_name.path, 'r') as url:
			df = pd.read_excel(obj.file_name)
			dfnew = df.fillna(value=0)
			#print(dfnew)
			
			for i, row in dfnew.iterrows():
				if i >= 3:
					
					
					fechaapli = row[1] #Fecha de aplicación
					tipodoc = row[2].strip() #Eliminar caracteres en blanco al inicio y final
					if tipodoc != 'NONE' and tipodoc != 0:
						tbltipodoc = Tipodoc.objects.filter(codigo = tipodoc).first()
					else:
						raise Exception('spam','Tipo de documento no existe')

					ident = str(row[3]) #Identificacion
					nombre1 = row[4]
					if row[5] != 'NONE' and row[5] != 0:
						nombre2 = row[5] #nombre2
					else:
						nombre2 = ""

					apel1 = row[6]
					if row[7] != 'NONE' and row[7] != 0:
						apel2 = row[7]
					else:
						apel2 = ""

					fechanac = row[8] #Fecha de nacimiento
					edadanios = row[9] #Edad Años
					edadmes = row[10] #Edad mes
					edaddias = row[11] #Edad día
					edadtotalmeses = row[12] #Edad Total mes
					sexo = row[14]
					if sexo == "HOMBRE":
						sexo = 'Masculino'
					else:
						sexo = "Femenino"
						
					paisnac = row[18]

					
					regimen = row[21] #Regimen de afiliación
					eps = row[22] #EAPB
					etnia = row[23]
					desplazado = row[24]
					discapacitado = row[25]
					fallecido = row[26]					
					victima = row[27]
					estudiante = row[28]

					dptores = row[30]
					mpioRes = row[31]
					barriores = row[32] #Barrio o localidad
					area = row[33] #Area Urbana o Rural
					direccion = row[34] #dirección
					telefono = row[36] #telefono
					email = row[37] #Correo electronico
					if not (email != 'NONE' and email != 0):
						email=''	

					autorizallamada = row[38]	
					autorizaenvemail = row[39]	

					namevacunador = row[252]
					registroenpaiweb = row[253]					
					observacion = row[255]

					#Area de buscar las tablas complementarias
					paisn = Pais.objects.filter(descripcion=paisnac).first() 
					deptores = Municipio.objects.filter(descripcion=dptores).first() 						
					munres = Municipio.objects.filter(descripcion=mpioRes).first() 	
					barrio = Barrio.objects.filter(descripcion=barriores).first() 	
					tblarea = Area.objects.filter(descripcion=area).first() 	
					tblreg = Regimen.objects.filter(descripcion=regimen).first() 	
					tbleps = Eps.objects.filter(descripcion=eps).first() 	
					tbletnia = Etnia.objects.filter(descripcion=etnia).first() 	
					tblsexo = Sexo.objects.filter(descripcion=sexo).first() 	

					pac = Paciente.objects.filter(tipodoc=tbltipodoc).filter(identificacion=ident).first()
					if pac:
						if pac.direccion == '':
							pac.direccion = direccion
						if pac.telefono=='':
							pac.telefono = telefono
						if pac.correoelectronico == '':
							pac.correoelectronico = email						
						pac.save()	

					else:
						pac = Paciente()
						if tbltipodoc:
							pac.tipodoc = tbltipodoc
						pac.identificacion = ident
						pac.nombre1 = nombre1
						pac.nombre2 = nombre2
						pac.apellido1 = apel1
						pac.apellido2 = apel2
						pac.fechaNac = fechanac
						if paisn:
							pac.pais = paisn
						if deptores:
							pac.departamento = deptores
						if munres:
							pac.municipio = munres
						pac.direccion = direccion #dirección
						pac.telefono = telefono #Teléfono
						if email != 'NONE' and email != 0:
							pac.correoelectronico = email #email
						if barrio:
							pac.barrio = barrio
						if tblarea:
							pac.area = tblarea
						if tblreg:
							pac.regimen = tblreg
						if tbleps:
							pac.eps = tbleps
						if tblsexo:
							pac.sexo = tblsexo
						if tbletnia:
							pac.etnia = tbletnia
						pac.save()
						pac = Paciente.objects.filter(tipodoc=tbltipodoc).filter(identificacion=ident).first()

						pacobj.append(pac.razonsocial)

					print("Datos del paciente: ", pac.razonsocial)
					red = Rediarioregular.objects.filter(fecha=fechaapli).filter(paciente=pac).first()

					if not red:
						linea.append([fechaapli,tipodoc, ident,fechanac,apel1, apel2, nombre1, nombre2])						
						red = Rediarioregular()						
						red.ips = btlips
						red.fecha = fechaapli 
						red.paciente = pac
						red.edadanios = edadanios
						red.edadmes = edadmes
						red.edaddias = edaddias
						red.edadtotalmeses = edadtotalmeses
						red.desplazado = desplazado
						red.discapacitado = discapacitado
						red.fallecido = fallecido
						red.victima = victima
						red.estudiante = estudiante
						red.autorizallamada = autorizallamada
						red.autorizaenvemail = autorizaenvemail
						#red.madre = desplazado
						#red.cuidador = desplazado
						red.namevacunador = namevacunador
						red.registroenpaiweb = registroenpaiweb
						red.observacion=observacion
						red.save()
						
					nrofrascos=0
					red = Rediarioregular.objects.filter(fecha=fechaapli).filter(paciente=pac).first()
					if red:
					# Para VIP
						dosisbiol = row[93] #Dosis del biologico polio inyectable
						lotebiol = row[94] #Lote del biologico polio inyectable
						jeringa = row[95] #Clase de jeringa
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[96] #Lote del biologico polio inyectable
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='VPI').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)

					# Para POLIO ORAL
						dosisbiol = row[98] #Dosis del biologico polio ORAL
						lotebiol = row[94] #Lote del biologico polio Oral
						jeringa = ''
						if jeringa:
							jeringa = jeringa
						lotejeringa = ''
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='VOP').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)							
					
					# Para PENTAVALENTE
						dosisbiol = row[101] #Dosis del biologico polio ORAL
						lotebiol = row[102] #Lote del biologico polio Oral
						jeringa = row[103]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[104]
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='PENTA').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)							
					
					#Pendiente Hexavalente
					# Para DTP
						dosisbiol = row[110] #Dosis del biologico polio ORAL
						lotebiol = row[111] #Lote del biologico polio Oral
						jeringa = row[112]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[113]
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='DPT').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)							
							
					# Para DTP ACELULAR	
						dosisbiol = row[114] #Dosis del biologico polio ORAL
						lotebiol = row[115] #Lote del biologico polio Oral
						jeringa = row[116]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[117]
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='DPTAP').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)							
					# Pendiente TD PEDIATRICO

					# Para ROTAVIRUS
						dosisbiol = row[122] #Dosis del biologico polio ORAL
						lotebiol = row[123] #Lote del biologico polio Oral
						jeringa = ''
						if jeringa:
							jeringa = jeringa
						lotejeringa = ''
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='ROTA').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)							

					# Para NEUMOCOCO
						dosisbiol = row[125] #Dosis del biologico polio ORAL
						lotebiol = row[126] #Lote del biologico polio Oral
						jeringa = row[127]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[128]
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='NEUMO').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)

					# Para Triple viral - SRP
						dosisbiol = row[129] #Dosis del biologico polio ORAL
						lotebiol = row[130] #Lote del biologico polio Oral
						jeringa = row[131]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[132]
						lotediluyente = row[133]						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='SRP').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)


					#Sarampión - Rubeola - SR Multidosis							
						dosisbiol = row[134] #Dosis del biologico polio ORAL
						lotebiol = row[135] #Lote del biologico polio Oral
						jeringa = row[136]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[137]
						lotediluyente = row[138]						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='SR').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)

					#Fiebre Amarilla	
						dosisbiol = row[139] #Dosis del biologico polio ORAL
						lotebiol = row[140] #Lote del biologico polio Oral
						jeringa = row[141]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[142]
						lotediluyente = row[143]						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='FA').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						

					#Hepatitis A pediátrica 	
						dosisbiol = row[144] #Dosis del biologico polio ORAL
						lotebiol = row[145] #Lote del biologico polio Oral
						jeringa = row[146]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[147]
						lotediluyente = None						
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='HA').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						

					# VARICELA
						dosisbiol = row[148] #Dosis del biologico polio ORAL
						lotebiol = row[149] #Lote del biologico polio Oral
						jeringa = row[150]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[151]
						lotediluyente = row[152]				
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='VAR').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						

					#Toxoide tetánico y diftérico de Adulto
						dosisbiol = row[153] #Dosis del biologico polio ORAL
						lotebiol = row[154] #Lote del biologico polio Oral
						jeringa = row[155]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[156]
						lotediluyente = None				
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='TDAD').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						

					#dTpa adulto 
						dosisbiol = row[157] #Dosis del biologico dTpa adulto 
						lotebiol = row[158] #Lote del biologico dTpa adulto 
						jeringa = row[159]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[160]
						lotediluyente = None				
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='DTPAD').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						

					#Influenza
						dosisbiol = row[161] #Dosis del biologico Influenza
						lotebiol = row[162] #Lote del biologico Influenza
						jeringa = row[163]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[164]
						lotediluyente = None				
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='INF').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						
					#VPH 
						dosisbiol = row[166] #Dosis del biologico VPH
						lotebiol = row[167] #Lote del biologico VPH
						jeringa = row[168]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[169]
						lotediluyente = None				
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='VPH').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						
						
					#Antirrábica  Humana (vacuna) 
						dosisbiol = row[170] #Dosis del biologico Antirrábica  Humana (vacuna) 
						lotebiol = row[171] #Lote del biologico Antirrábica  Humana (vacuna) 
						jeringa = row[172]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[173]
						lotediluyente = row[174]				
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='AH').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						

					#Antirrábico Humano (suero) 
						dosisbiol = '' 
						nrofrascos = row[176] #Dosis del biologico Antirrábica  Humana (vacuna) 
						lotebiol = row[177] #Lote del biologico Antirrábica  Humana (vacuna) 
						jeringa = ''
						if jeringa:
							jeringa = jeringa
						lotejeringa = ''
						lotediluyente = None				
						if nrofrascos != 0:
							tblbiol = Biologico.objects.filter(codigo='AHS').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						


					#Hepatitis B (Inmunoglobulina)
						dosisbiol = row[178] #Dosis del biologico Antirrábica  Humana (vacuna) 
						lotebiol = row[179] #Lote del biologico Antirrábica  Humana (vacuna) 
						jeringa = row[180]
						if jeringa:
							jeringa = jeringa
						lotejeringa = row[181]
						lotediluyente = None			
						if dosisbiol != 0:
							tblbiol = Biologico.objects.filter(codigo='HEPBINM').first()
							resultado = insertar_dosis_biologico(tblbiol, red, dosisbiol, lotebiol, jeringa, lotejeringa, lotediluyente, nrofrascos)						


			contexto.update({'dfc':linea, 'pac':pacobj})		

		obj.activated = True
		obj.save()
		return redirect('pai:rediario_reg_list')

	return render(request,template, contexto) 

def listar_rediario_regular(request):	
	template = 'pai/rediario_regular_list.html'
	contexto = {}
	if request.method == 'POST':
		ident = request.POST.get('dato')
		rediario = Rediarioregular.objects.filter(paciente__identificacion = ident).all()			
	else:	
		rediario = Rediarioregular.objects.all()	
	contexto.update({'obj':rediario})	
	return render(request,template,contexto)








