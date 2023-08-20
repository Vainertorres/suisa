from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import generic
from django.db.models import Count
from datetime import datetime
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum

import folium
from folium.plugins import MarkerCluster
from folium import plugins
from folium.plugins import HeatMap
import pandas as pd
import webbrowser


from cnf.views import Sin_privilegio
from cnf.models import Ips, Tipodoc, Departamento, Municipio, Regimen, UmEdad, Sexo, Area, Eps, \
Paciente

from .forms import ImportCie10Form, PeriodoImportRipsForm,DiagnosticosForm
from .models import Diagnosticos, ImportarCie10, PeriodoImportRips, RipsControl, RipsUsuarios, \
RipsConsulta, Finalidad,CausaExterna, Cups, DiagRipsCons, TipoDiagPrincipal, Tipousuario, RipsProcedimiento, \
FormaRealizactoQx, PersonalAsistencial, FinalidadProcedimiento, AmbitoProcedimiento, DiagProcedimiento, \
RipsUrgencia, DiagRipsUrgencia, DestinoSalida, EstadoSalida, ViaIngreso, RipsHospitalizacion, \
DiagRipsHospitaliza, RipsMedicamento, RipsTransaccion, RipsOtrosServicios, \
TipoServicio


# Create your views here.

class Home(generic.TemplateView):
	template_name= 'base/baserips.html'


class Grafdiagnosticoscie10(generic.TemplateView):
	template_name='bai/estdiagcoomorbilidad_form.html'

	def reporteDiagnosticos(self):

		estcie = DiagRipsCons.objects.values('diagnostico__codigo','diagnostico__descripcion').annotate(cant=Count('id')).order_by("-cant")		
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			descdx = x['diagnostico__codigo']
			namediag = x['diagnostico__descripcion']
			if cant > 0:
				diccionario = {'name':namediag ,'y':cant}
				data.append(diccionario)

		return data

	def reporteDiagnosticosdb(self):

		estcie = DiagRipsCons.objects.values('diagnostico__codigo', 'diagnostico__descripcion').annotate(cant=Count('id')).order_by("-cant")				
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			descdx = x['diagnostico__codigo']
			nombredx=x['diagnostico__descripcion']
			
			if cant > 0:
				diccionario = {'name':descdx, 'nombredx':nombredx, 'y':cant}
				data.append(diccionario)

		return data

	def reporteFinalidad(self):
		estcie = RipsConsulta.objects.values('finalidad__descripcion').annotate(cant=Count('id'))
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			namefinalidad = x['finalidad__descripcion']
			if cant > 0:
				diccionario = {'name':namefinalidad,'y':cant}
				data.append(diccionario)

		return data

	def reporteCausaExterna(self):
		estcie = RipsConsulta.objects.values('causaExterna__descripcion').annotate(cant=Count('id'))
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			namefinalidad = x['causaExterna__descripcion']
			if cant > 0:
				diccionario = {'name':namefinalidad,'y':cant}
				data.append(diccionario)

		return data

	def reporteTipoconsulta(self):
		estcie = RipsConsulta.objects.values('cups__descripcion').annotate(cant=Count('id'))
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			namecups = x['cups__descripcion']
			if cant > 0:
				diccionario = {'name':namecups,'y':cant}
				data.append(diccionario)
		return data

	def reporteSexo(self):
		estcie = RipsConsulta.objects.values('paciente__sexo__descripcion').annotate(cant=Count('id'))
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			namesexo = x['paciente__sexo__descripcion']
			if namesexo == None:
				namesexo="Sin dato"

			if cant > 0:
				diccionario = {'name':namesexo,'y':cant}
				data.append(diccionario)
		return data


	def reporteEtnia(self):
		estcie = RipsConsulta.objects.values('paciente__etnia__descripcion').annotate(cant=Count('id'))
		
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			nameetnia = x['paciente__etnia__descripcion']
			if nameetnia == None:
				nameetnia="Sin dato"
			if cant > 0:
				diccionario = {'name':nameetnia,'y':cant}
				data.append(diccionario)
		return data

	def reporteBarrio(self):
		estcie = RipsConsulta.objects.values('paciente__barrio__descripcion').annotate(cant=Count('id'))
		print(estcie)
		diccionario = {}
		data = []
		for x in estcie:
			cant = x['cant']
			namebarrio = x['paciente__barrio__descripcion']
			if namebarrio == None:
				namebarrio="Sin dato"

			if cant > 0:
				diccionario = {'name':namebarrio,'y':cant}
				data.append(diccionario)
		return data
			
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['cie10']= self.reporteDiagnosticos()
	    context['finalidad']= self.reporteFinalidad()
	    context['causaexterna']= self.reporteCausaExterna()
	    context['reportetipoconsulta']= self.reporteTipoconsulta()
	    context['cie10db']= self.reporteDiagnosticosdb()   
	    context['sexo']= self.reporteSexo()
	    context['etnia']= self.reporteEtnia()
	    context['barrio']= self.reporteBarrio()

	    return context

class DiagnosticoList(Sin_privilegio, generic.ListView):
    permission_required="bai.view_diagnostico"
    model = Diagnosticos
    template_name='bai/diagnostico_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class DiagnosticoUpdate(Sin_privilegio, generic.UpdateView):
	permission_required="bai.change_diagnostico"
	model = Diagnosticos
	template_name = 'bai/diagnostico_form.html'
	context_object_name = 'obj'
	form_class = DiagnosticosForm	
	success_url = reverse_lazy('bai:cie10list')
	login_url = 'cnf:login'

class DiagnosticoCreate(Sin_privilegio, generic.CreateView):
	permission_required="bai.add_diagnostico"
	model = Diagnosticos
	template_name = 'bai/diagnostico_form.html'
	context_object_name = 'obj'
	form_class = DiagnosticosForm	
	success_url = reverse_lazy('bai:cie10list')
	login_url = 'cnf:login'


def importCie10(request):
	form = ImportCie10Form(request.POST or None, request.FILES or None)
	template='bai/importcie10.html'
	contexto = {'form':form} 

	def importarCie10(filecie10):
		df = pd.read_excel(filecie10)
		dfnew = df.fillna(value=0)
				
		for i, row in dfnew.iterrows():
			idcap = row['idcapitulo']
			capitulo = row['capitulo']
			idgrupo = row['idgrupo']
			grupo = row['grupo']
			codcie10 = row['codcie10']
			descripcion = row['descripcion']

			diag = Diagnosticos.objects.filter(codigo=codcie10).first()
			if diag:
				pass
			else:
				diag = Diagnosticos(
					codigo = codcie10,
					descripcion = descripcion,
					idcapitulo = idcap,
					capitulo = capitulo,
					codcie3 = idgrupo,
					descripcie3 = grupo
					)
				if diag:
					diag.save()

	def importarCups(fileCups):
		df = pd.read_excel(fileCups)
		dfnew = df.fillna(value=0)
				
		for i, row in dfnew.iterrows():
			codcups = row['codigo']
			descups = row['descripcion']

			cups = Cups.objects.filter(codigo=codcups).first()
			if cups:
				pass
			else:
				savecums = Cums()				
				savecums.save()

	def importarCums(fileCums):
		df = pd.read_excel(fileCums)
		dfnew = df.fillna(value=0)
				
		for i, row in dfnew.iterrows():
			codcups = row['codigo']
			descups = row['descripcion']

			cups = Cums.objects.filter(codigo=codcups).first()
			if cups:
				pass
			else:
				savecups = Cups()
				savecups.codigo = codcups
				savecups.descripcion = descups
				savecups.save()

	if form.is_valid():
		form.save()
		form = ImportCie10Form()
		obj = ImportarCie10.objects.get(activated=False)
		filecie10 =  obj.file_name
		filecups = obj.file_cups
		filecums = obj.file_cums


		if obj.file_name:
			importarCie10(obj.file_name)
		if obj.file_cups:
			importarCups(obj.file_cups)
		if obj.file_cums:
			importarCums(obj.file_cums)
					
		obj.activated=True				
		obj.save()
		template = 'bai/diagnostico_list.html'
		diag = Diagnosticos.objects.all()
		contexto = {'obj':diag}
		return render(request,template,contexto )

	return render(request,template, contexto)



def importRips(request):
	form = PeriodoImportRipsForm(request.POST or None, request.FILES or None)
	template='bai/importRips.html'
	contexto = {'form':form} 	

	def importarCT(fileCT, periodo):
		with open(fileCT.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 			
			dfnew = df.fillna(value=0)						
			for i, row in dfnew.iterrows():
				codprestador = row[0]
				fecrem = periodo.fecharemision
				codfile = row[2]
				totreg = row[3]

				ips = Ips.objects.filter(codhabilitacion=codprestador).first()
				ripsct = RipsControl.objects.filter(ips_id = ips.pk).filter(fecharemision=fecrem).filter(codarchivo=codfile).first()
				if ripsct:
					pass
				else:
					ripsct = RipsControl(
					ips = ips,
					fecharemision=fecrem,
					codarchivo=codfile,
					totalreg=totreg,
					periodoimportRips = periodo
					)
					if ripsct:
						ripsct.save()

	def importar_usuario(fileUS):
		with open(fileUS.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 
			
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				tipodoc = row[0]
				ident = row[1]
				codeps = row[2]
				codtipouser = row[3]
				apel1 = row[4]
				apel2 = row[5]
				nom1 = row[6]
				nom2 = row[7]
				edad = row[8]
				umedad = row[9]				
				sexo = row[10]
				coddpto = row[11]
				codmpio = row[12]
				codzona = row[13]
				td = Tipodoc.objects.filter(codigo=tipodoc).first()
				eps = Eps.objects.filter(codigo=codeps).first()
				tipouser = Tipousuario.objects.filter(codigo=codtipouser).first()
				umed = UmEdad.objects.filter(codigo=umedad).first()
				sex = Sexo.objects.filter(codigo=sexo).first()
				dpto = Departamento.objects.filter(codigo=coddpto).first()
				mpio = Municipio.objects.filter(codigo=codmpio).first()
				area = Area.objects.filter(codigo=codzona).first()
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.pk).filter(identificacion=ident).first()
				if ripsuser:
					pass
				else:
					ripsuser = RipsUsuarios()
					ripsuser.tipodoc = td
					ripsuser.identificacion = ident
					if eps:
						ripsuser.eps = eps
					if tipouser:
						ripsuser.tipousuario = tipouser
					ripsuser.apellido1 = apel1 
					ripsuser.apellido2 = apel2
					ripsuser.nombre1 = nom1
					ripsuser.nombre2 = nom2
					ripsuser.edad = edad
					if umed:
						ripsuser.umedad = umed
					if sex:
						ripsuser.sexo = sex
					if dpto:
						ripsuser.departamento = dpto
					if mpio:
						ripsuser.municipio = mpio
					if area:
						ripsuser.area = area
					ripsuser.save()


	def importfileAC(fileAC, periodo):

		with open(fileAC.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				nrofac = row[0]
				codprestador = row[1]
				tipodoc = row[2]
				ident = row[3]				
				fechcons = datetime.strptime(row[4], '%d/%m/%Y') 
				nroautoriza = row[5]
				codcups = row[6]
				codfinalidad = row[7]
				if codfinalidad < 10:
					codfinalidad='0'+str(codfinalidad)

				codcausaext = row[8]
				if codcausaext < 10:
					codcausaext = '0'+str(codcausaext)
				coddxppal = row[9]
				coddxrel1 = row[10]
				coddxrel2 = row[11]
				coddxrel3 = row[12]
				tipodxppal = row[13]
				vlrconsulta = row[14]
				vlrctamoderadora = row[15]			
				vlrnetopagar = row[16]
				pruebafecha = periodo.fecharemision
				ips = Ips.objects.filter(codhabilitacion=codprestador).first()
				td = Tipodoc.objects.filter(codigo=tipodoc).first()			
				pac = Paciente.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				umedad = ripsuser.umedad
				finalidad = Finalidad.objects.filter(codigo=codfinalidad).first()
				causaext = CausaExterna.objects.filter(codigo=codcausaext).first()
				cups = Cups.objects.filter(codigo=codcups).first();
				ripsac = RipsConsulta.objects.filter(paciente_id=pac.id).filter(fechacons=fechcons).first()

				if ripsac:
					pass
				else:
					ripsac = RipsConsulta()
					ripsac.nrofactura = nrofac
					if ips:
						ripsac.ips = ips
					if pac:
						ripsac.paciente = pac
					ripsac.fechacons = fechcons
					ripsac.nroautoriza = nroautoriza
					if cups:
						ripsac.cups = cups
					if finalidad:
						ripsac.finalidad = finalidad
					if causaext:
						ripsac.causaExterna = causaext
					ripsac.vlrconsulta = vlrconsulta
					ripsac.vlrcuotamodera = vlrctamoderadora
					ripsac.vlrneto = vlrnetopagar
					if ripsuser:
						ripsac.edad = ripsuser.edad
						ripsac.umEdad = ripsuser.umedad
					ripsac.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AC").first()

					if rcontrol:
						print(rcontrol)
						ripsac.ripscontrol = rcontrol
					ripsac.save()


					dxppal = Diagnosticos.objects.filter(codigo=coddxppal).first()
					diarel1 = Diagnosticos.objects.filter(codigo=coddxrel1).first()
					diarel2 = Diagnosticos.objects.filter(codigo=coddxrel2).first()
					diarel3 = Diagnosticos.objects.filter(codigo=coddxrel3).first()
					if dxppal: #diagnostico Principal
						tdppal = TipoDiagPrincipal.objects.filter(codigo=tipodxppal).first()
						dxcons = DiagRipsCons()
						dxcons.diagnostico = dxppal
						dxcons.ripsconsulta  = ripsac
						dxcons.diagppal = 'SI'
						if tdppal:
							dxcons.tipodiagppal = tdppal
						dxcons.save()
					if diarel1: #diagnostico relacionado 1					
						dxcons = DiagRipsCons()
						dxcons.diagnostico = diarel1
						dxcons.ripsconsulta  = ripsac
						dxcons.diagppal = 'NO'					
						dxcons.save()
					if diarel2: #diagnostico relacionado 2	
						dxcons = DiagRipsCons()
						dxcons.diagnostico = diarel2
						dxcons.ripsconsulta  = ripsac
						dxcons.diagppal = 'NO'					
						dxcons.save()
					if diarel3: #diagnostico relacionado 2	
						dxcons = DiagRipsCons()
						dxcons.diagnostico = diarel3
						dxcons.ripsconsulta  = ripsac
						dxcons.diagppal = 'NO'					
						dxcons.save()

	def importfileAP(fileAP, periodo):
		with open(fileAP.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				nrofac = row[0]
				codprestador = row[1]
				tipodoc = row[2]
				ident = row[3]				
				fechaproc = datetime.strptime(row[4], '%d/%m/%Y') 
				nroautoriza = row[5]
				codcups = row[6]
				codambitorealizaproc = row[7]
				codfinalidadproc = row[8]
				codpersonalatiende = row[9]
				coddxppal = row[10]
				coddxrel = row[11]
				coddxcomplicacion = row[12]
				codformarealizactoqx = row[13]				
				vlrprocedimieto = row[14]
				
				pruebafecha = periodo.fecharemision
				
				ips = Ips.objects.filter(codhabilitacion=codprestador).first()
				td = Tipodoc.objects.filter(codigo=tipodoc).first()			
				pac = Paciente.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()				
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				cups = Cups.objects.filter(codigo=codcups).first();
				ambitorealproc = AmbitoProcedimiento.objects.filter(codigo=codambitorealizaproc).first()
				finalidad = FinalidadProcedimiento.objects.filter(codigo=codfinalidadproc).first()
				personalatiende = PersonalAsistencial.objects.filter(codigo=codpersonalatiende).first()
				formarealizactoqx = FormaRealizactoQx.objects.filter(codigo=codformarealizactoqx).first()

				ripsap = RipsProcedimiento.objects.filter(paciente_id=pac.id).filter(fechaprocedimiento=fechaproc).filter(cups_id=cups.id).first()

				if ripsap: #tener presente para establecer maneras de validar que no se carguen datos demás
					ripsap = RipsProcedimiento()
					ripsap.nrofactura = nrofac
					if ips:
						ripsap.ips = ips
					if pac:
						ripsap.paciente = pac
					ripsap.fechaprocedimiento = fechaproc
					ripsap.nroautoriza = nroautoriza
					if cups:
						ripsap.cups = cups

					if ambitorealproc: #Ambito de realizacion del procedimiento
						ripsap.ambitoprocedimiento = ambitorealproc

					if finalidad: #finalidad del procedimiento
						ripsap.finalidad = finalidad
	
					if personalatiende: #Personal que atiende
						ripsap.personalasistencial = personalatiende

					if formarealizactoqx: #Forma de realización del acto quirurgico
						ripsap.formarealizactoqx = formarealizactoqx

					ripsap.valorprocedimiento = vlrprocedimieto
					
					ripsap.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AP").first()

					if rcontrol:						
						ripsap.ripscontrol = rcontrol
					ripsap.save()


					dxppal = Diagnosticos.objects.filter(codigo=coddxppal).first()
					diarel = Diagnosticos.objects.filter(codigo=coddxrel).first()
					diagcompl = Diagnosticos.objects.filter(codigo=coddxcomplicacion).first()
					
					if dxppal: #diagnostico Principal						
						dxProc = DiagProcedimiento()
						dxProc.diagnostico = dxppal
						dxProc.ripsprocedimiento  = ripsap
						dxProc.diagppal = 'DP'						
						dxProc.save()
					if diarel: #diagnostico relacionado 1					
						dxProc = DiagProcedimiento()
						dxProc.diagnostico = diarel
						dxProc.ripsprocedimiento  = ripsap
						dxProc.diagppal = 'DR'						
						dxProc.save()
					if diagcompl: #diagnostico relacionado 2	
						dxProc = DiagProcedimiento()
						dxProc.diagnostico = diagcompl
						dxProc.ripsprocedimiento  = ripsap
						dxProc.diagppal = 'DC'						
						dxProc.save()
				else:
					ripsap = RipsProcedimiento()
					ripsap.nrofactura = nrofac
					if ips:
						ripsap.ips = ips
					if pac:
						ripsap.paciente = pac
					ripsap.fechaprocedimiento = fechaproc
					ripsap.nroautoriza = nroautoriza
					if cups:
						ripsap.cups = cups

					if ambitorealproc: #Ambito de realizacion del procedimiento
						ripsap.ambitoprocedimiento = ambitorealproc

					if finalidad: #finalidad del procedimiento
						ripsap.finalidad = finalidad
	
					if personalatiende: #Personal que atiende
						ripsap.personalasistencial = personalatiende

					if formarealizactoqx: #Forma de realización del acto quirurgico
						ripsap.formarealizactoqx = formarealizactoqx

					ripsap.valorprocedimiento = vlrprocedimieto
					
					ripsap.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AP").first()

					if rcontrol:						
						ripsap.ripscontrol = rcontrol
					ripsap.save()


					dxppal = Diagnosticos.objects.filter(codigo=coddxppal).first()
					diarel = Diagnosticos.objects.filter(codigo=coddxrel).first()
					diagcompl = Diagnosticos.objects.filter(codigo=coddxcomplicacion).first()
					
					if dxppal: #diagnostico Principal						
						dxProc = DiagProcedimiento()
						dxProc.diagnostico = dxppal
						dxProc.ripsprocedimiento  = ripsap
						dxProc.diagppal = 'DP'						
						dxProc.save()
					if diarel: #diagnostico relacionado 1					
						dxProc = DiagProcedimiento()
						dxProc.diagnostico = diarel
						dxProc.ripsprocedimiento  = ripsap
						dxProc.diagppal = 'DR'						
						dxProc.save()
					if diagcompl: #diagnostico relacionado 2	
						dxProc = DiagProcedimiento()
						dxProc.diagnostico = diagcompl
						dxProc.ripsprocedimiento  = ripsap
						dxProc.diagppal = 'DC'						
						dxProc.save()

#Fin funcion de procedimientos


	def importfileAU(fileAU, periodo):
		with open(fileAU.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 	
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				nrofac = row[0]
				codprestador = row[1]
				tipodoc = row[2]
				ident = row[3]				
				fechaingreso = datetime.strptime(row[4], '%d/%m/%Y') 
				horaingreso = datetime.strptime(row[5], '%H:%M') 
				nroautoriza = row[6]
				codcausaext = row[7]
				if codcausaext < 10:
					codcausaext = '0'+str(codcausaext)
				diagppal = row[8]
				diagrel1 = row[9]
				diagrel2 = row[10]
				diagrel3 = row[11]
				destsal = row[12]
				estsal = row[13]
				dxmuerte = row[14]
				fechaegreso = datetime.strptime(row[15], '%d/%m/%Y') 
				horaegreso = datetime.strptime(row[16], '%H:%M') 
				
				ips = Ips.objects.filter(codhabilitacion=codprestador).first()
				td = Tipodoc.objects.filter(codigo=tipodoc).first()			
				pac = Paciente.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				causaexterna = CausaExterna.objects.filter(codigo=codcausaext).first()
				destinasal = DestinoSalida.objects.filter(codigo=destsal).first()
				estadosal = EstadoSalida.objects.filter(codigo=estsal).first()
				diagmuerte = Diagnosticos.objects.filter(codigo=dxmuerte).first()

				
				ripsau = RipsUrgencia.objects.filter(paciente_id=pac.id).filter(fechaingreso=fechaingreso).first()

				if ripsau:
					pass
				else:
					ripsau = RipsUrgencia()
					ripsau.nrofactura = nrofac
					if ips:
						ripsau.ips = ips
					if pac:
						ripsau.paciente = pac
					ripsau.fechaingreso = fechaingreso
					ripsau.horaingreo = horaingreso

					ripsau.nroautoriza = nroautoriza
					if causaexterna:
						ripsau.causaexterna = causaexterna
					if destinasal:
						ripsau.destinosalida = destinasal
					if estadosal:
						ripsau.estadosalida = estadosal
					if diagmuerte:
						ripsau.diagmuerte = diagmuerte
					
					ripsau.fechasalida = fechaegreso
					ripsau.horasalida = horaegreso

					ripsau.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AU").first()

					if rcontrol:						
						ripsau.ripscontrol = rcontrol
					ripsau.save()


					dxppal = Diagnosticos.objects.filter(codigo=diagppal).first()
					diarel1 = Diagnosticos.objects.filter(codigo=diagrel1).first()
					diarel2 = Diagnosticos.objects.filter(codigo=diagrel2).first()
					diarel3 = Diagnosticos.objects.filter(codigo=diagrel3).first()

					
					if dxppal: #diagnostico Principal						
						dxUrg = DiagRipsUrgencia()
						dxUrg.diagnostico = dxppal
						dxUrg.ripsurgencia  = ripsau
						dxUrg.diagppal = 'SI'						
						dxUrg.save()
					if diarel1: #diagnostico relacionado 1					
						dxUrg = DiagRipsUrgencia()
						dxUrg.diagnostico = diarel1
						dxUrg.ripsurgencia  = ripsau
						dxUrg.diagppal = 'NO'						
						dxUrg.save()
					if diarel2: #diagnostico relacionado 2	
						dxUrg = DiagRipsUrgencia()
						dxUrg.diagnostico = diarel2
						dxUrg.ripsurgencia  = ripsau
						dxUrg.diagppal = 'NO'						
						dxUrg.save()
					if diarel3: #diagnostico relacionado 3	
						dxUrg = DiagRipsUrgencia()
						dxUrg.diagnostico = diarel3
						dxUrg.ripsurgencia  = ripsau
						dxUrg.diagppal = 'NO'						
						dxUrg.save()

#Fin funcion de Rips de servicios de urgencias.

	def importfileAH(fileAH, periodo):
		with open(fileAH.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 	
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				nrofac = row[0]
				codprestador = row[1]
				tipodoc = row[2]
				ident = row[3]
				viaingreso = row[4]				
				fechaingreso = datetime.strptime(row[5], '%d/%m/%Y') 
				horaingreso = datetime.strptime(row[6], '%H:%M') 
				nroautoriza = row[7]
				codcausaext = row[8]
				if codcausaext < 10:
					codcausaext = '0'+str(codcausaext)
				diagppalingreso = row[9]
				diagppalegreso = row[10]
				diagrel1egre = row[11]
				diagrel2egre = row[12]
				diagrel3egre = row[13]
				diagcomplica = row[14]
				estsal = row[15]
				dxmuerte = row[16]
				fechaegreso = datetime.strptime(row[17], '%d/%m/%Y') 
				horaegreso = datetime.strptime(row[18], '%H:%M') 
				
				ips = Ips.objects.filter(codhabilitacion=codprestador).first()
				td = Tipodoc.objects.filter(codigo=tipodoc).first()			
				pac = Paciente.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				viaing = ViaIngreso.objects.filter(codigo=viaingreso).first()
				causaexterna = CausaExterna.objects.filter(codigo=codcausaext).first()
				diagppaling = Diagnosticos.objects.filter(codigo=diagppalingreso).first()
				diagcompli = Diagnosticos.objects.filter(codigo=diagcomplica).first()
				estadosal = EstadoSalida.objects.filter(codigo=estsal).first()
				diagmuerte = Diagnosticos.objects.filter(codigo=dxmuerte).first()

				
				ripsah = RipsHospitalizacion.objects.filter(paciente_id=pac.id).filter(fechaingreso=fechaingreso).first()

				if ripsah:
					pass
				else:
					ripsah = RipsHospitalizacion()
					ripsah.nrofactura = nrofac
					if ips:
						ripsah.ips = ips
					if pac:
						ripsah.paciente = pac
					if viaing:
						ripsah.viaingreso = viaing

					ripsah.fechaingreso = fechaingreso
					ripsah.horaingreo = horaingreso

					ripsah.nroautoriza = nroautoriza
					if causaexterna:
						ripsah.causaexterna = causaexterna

					if diagppaling:
						ripsah.diagppalingreso = diagppaling

					if diagcompli:
						ripsah.diagcomplicaciones = diagcompli

					if estadosal:
						ripsah.estadosalida = estadosal

					if diagmuerte:
						ripsah.diagmuerte = diagmuerte
					
					ripsah.fechasalida = fechaegreso
					ripsah.horasalida = horaegreso

					ripsah.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AH").first()

					if rcontrol:						
						ripsah.ripscontrol = rcontrol
					ripsah.save()


					dxppalegre = Diagnosticos.objects.filter(codigo=diagppalegreso).first()
					diarel1egre = Diagnosticos.objects.filter(codigo=diagrel1egre).first()
					diarel2egre = Diagnosticos.objects.filter(codigo=diagrel2egre).first()
					diarel3egre = Diagnosticos.objects.filter(codigo=diagrel3egre).first()

					
					if dxppalegre: #diagnostico Principal						
						dxHosp = DiagRipsHospitaliza()
						dxHosp.diagnostico = dxppalegre
						dxHosp.ripshospitalizacion  = ripsah
						dxHosp.diagppal = 'SI'						
						dxHosp.save()
					if diarel1egre: #diagnostico relacionado 1					
						dxHosp = DiagRipsHospitaliza()
						dxHosp.diagnostico = diarel1egre
						dxHosp.ripshospitalizacion  = ripsah
						dxHosp.diagppal = 'NO'						
						dxHosp.save()
					if diarel2egre: #diagnostico relacionado 2	
						dxHosp = DiagRipsHospitaliza()
						dxHosp.diagnostico = diarel2egre
						dxHosp.ripshospitalizacion  = ripsah
						dxHosp.diagppal = 'NO'						
						dxHosp.save()
					if diarel3egre: #diagnostico relacionado 3	
						dxHosp = DiagRipsHospitaliza()
						dxHosp.diagnostico = diarel3egre
						dxHosp.ripshospitalizacion  = ripsah
						dxHosp.diagppal = 'NO'						
						dxHosp.save()

#Fin funcion de Rips de servicios de Hospitalizacion.

	def importfileAM(fileAM, periodo):
		with open(fileAM.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 	
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				nrofac = row[0]
				codprestador = row[1]
				tipodoc = row[2]
				ident = row[3]
				nroautoriza = row[4]
				codmed = row[5]
				codtipomed = row[6]
				nomgenerico = row[7]
				formafarmaceutica = row[8]
				concentracionmed = row[9]
				unidadmed = row[10]
				nrounidades = row[11]
				vlrunitario = row[12]
				vlrtotal = row[13]
				
				ips = Ips.objects.filter(codhabilitacion=codprestador).first()
				td = Tipodoc.objects.filter(codigo=tipodoc).first()			
				pac = Paciente.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				medica = Cums.objects.filter(atc=codmed).first()
				
				ripsam = RipsMedicamento.objects.filter(paciente_id=pac.id).filter(nrofactura=nrofac).filter(cums_codigo=codmed).first()

				if ripsam:
					pass
				else:
					ripsam = RipsMedicamento()
					ripsam.nrofactura = nrofac
					if ips:
						ripsam.ips = ips
					if pac:
						ripsam.paciente = pac


					ripsam.nroautoriza = nroautoriza
					if medica:
						ripsam.cums = medica

					if diagppaling:
						ripsah.diagppalingreso = diagppaling

					if diagcompli:
						ripsah.diagcomplicaciones = diagcompli

					if estadosal:
						ripsah.estadosalida = estadosal

					if diagmuerte:
						ripsah.diagmuerte = diagmuerte
					
					ripsah.fechasalida = fechaegreso
					ripsah.horasalida = horaegreso

					ripsah.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AM").first()

					if rcontrol:						
						ripsah.ripscontrol = rcontrol
					ripsah.save()

				
#Fin funcion de Rips de Medicamentos.

	def importfileAF(fileAF, periodo):
		with open(fileAF.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 	
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				codhabprestador = row[0]
				nameprestador = row[1]
				tipodocprestador = row[2]
				nroidentprestador = row[3]
				nrofac = row[4]
				fechaexpfact = datetime.strptime(row[5], '%d/%m/%Y') 
				fechainicio = datetime.strptime(row[6], '%d/%m/%Y') 
				fechafinal = datetime.strptime(row[7], '%d/%m/%Y') 
				codeps = row[8]
				nameeps = row[9]
				nrocontrato = row[10]
				planbeneficio = row[11]
				nropoliza = row[12]
				vlrcopago = row[13]
				vlrcomision = row[14]
				vlrdescuento = row[15]
				vlrnetopagar = row[16]


				
				ips = Ips.objects.filter(codhabilitacion=codhabprestador).first()						
				eps = Eps.objects.filter(codigo=codeps).first()

				ripsaf = RipsTransaccion.objects.filter(ips_id=ips.id).filter(nrofactura=nrofac).first()

				if ripsaf:
					pass
				else:
					ripsaf = RipsTransaccion()
					ripsaf.nrofactura = nrofac
					ripsaf.fechaexpfac = fechaexpfact
					ripsaf.fechainicio = fechainicio
					ripsaf.fechafinal = fechafinal

					if ips:
						ripsaf.ips = ips
					if eps:
						ripsaf.eps = eps

					ripsaf.nrocontrato = nrocontrato
					ripsaf.planbeneficio = planbeneficio
					ripsaf.nropoliza = nropoliza
					ripsaf.vlrtotalcopago = vlrcopago
					ripsaf.vlrcomision = vlrcomision
					ripsaf.vlrdescuento = vlrdescuento
					ripsaf.vlrnetopagar = vlrnetopagar
					ripsaf.periodoimportrips = periodo
					rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AF").first()

					if rcontrol:						
						ripsaf.ripscontrol = rcontrol
					ripsaf.save()

#Fin funcion de Rips Transacciones.

#funcion importar rips otros servicios
	def importfileAT(fileAT, periodo):
		with open(fileAT.path, 'rt') as url:
			df = pd.read_csv(url, sep = ",",header=None, encoding = "ISO-8859-1", engine='python')		 	
			dfnew = df.fillna(value=0)
			for i, row in dfnew.iterrows():
				nrofac = row[0]
				codhabprestador = row[1]
				tipodoc = row[2]
				ident = row[3]
				nroautoriza = row[4]
				codtiposervicio = row[5]
				codservicio = row[6]
				descservicio = row[7]
				cantidad = row[8]
				vlrunitario = row[9]
				vlrtotal = row[10]

				ips = Ips.objects.filter(codhabilitacion=codhabprestador).first()		
				td = Tipodoc.objects.filter(codigo=tipodoc).first()			
				pac = Paciente.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()
				ripsuser = RipsUsuarios.objects.filter(tipodoc_id=td.id).filter(identificacion=ident).first()				
				dftiposerv = TipoServicio.objects.filter(codigo=codtiposervicio).first()

				#ripsat = RipsOtrosServicios.objects.filter(ips_id=ips.id).filter(nrofactura=nrofac).first()

				'''if ripsaf:
					pass
				else:'''
				ripsat = RipsOtrosServicios()
				ripsat.nrofactura = nrofac

				if ips:
					ripsat.ips = ips
				if pac:
					ripsat.paciente = pac
				ripsat.nroautoriza = nroautoriza

				if dftiposerv:
					ripsat.tiposervicio = dftiposerv

				ripsat.codigoservicio = codservicio
				ripsat.nombreservicio = descservicio
				ripsat.cantidad = cantidad
				ripsat.valorunitario = vlrunitario
				ripsat.valortotal = vlrtotal

				ripsat.periodoimportrips = periodo
				rcontrol = RipsControl.objects.filter(periodoimportRips=periodo, codarchivo__startswith="AT").first()

				if rcontrol:						
					ripsat.ripscontrol = rcontrol
				ripsat.save()

#Fin funcion de Rips Otros servicios.
	if form.is_valid():
		form.save()
		form = PeriodoImportRipsForm()
		obj = PeriodoImportRips.objects.get(activated=False)
		importarCT(obj.fileCT, obj)
		importar_usuario(obj.fileUS)
		if obj.fileAC:
			importfileAC(obj.fileAC, obj)
		if 	obj.fileAP:
			importfileAP(obj.fileAP, obj)
		if obj.fileAU:
			importfileAU(obj.fileAU, obj)
		if obj.fileAH:
			importfileAH(obj.fileAH, obj)
		if obj.fileAM:
			importfileAM(obj.fileAM, obj)
		if obj.fileAF:
			importfileAF(obj.fileAF, obj)
		if obj.fileAT:
			importfileAT(obj.fileAT, obj)
		
		obj.activated=True				
		obj.save()
		template = 'bai/archivoscontrol_list.html'
		ripsct = RipsControl.objects.filter(periodoimportRips_id=obj.id)
		contexto = {'obj':ripsct}
		return render(request,template,contexto )

	return render(request,template, contexto)

class Archivocontrolist(Sin_privilegio, generic.ListView):
	permission_required="bai.view_ripscontrol"
	model = RipsControl
	context_object_name='obj'
	template_name="bai/archivoscontrol_list.html"


class Archivoconsultalist(Sin_privilegio, generic.ListView):
	permission_required="bai.view_ripsconsulta"
	model = RipsConsulta
	context_object_name='obj'
	template_name="bai/archivosconsulta_list.html"

	def get_queryset(self):
		idripscontrol = self.request.GET.get("rc")
		qs = RipsConsulta.objects.filter(ripscontrol__id=idripscontrol).all()
		return qs
	
	def get_context_data(self, **kwargs):
		context = super(Archivoconsultalist,self).get_context_data(**kwargs)
		idripscontrol = self.request.GET.get("rc")
		qs = RipsControl.objects.filter(id=idripscontrol).first()
		context['ips'] = qs.ips
		return context 		


class ListadoDiagnostico(Sin_privilegio, generic.ListView):
	permission_required="bai.view_ripsconsulta"
	model = DiagRipsCons
	context_object_name='obj'
	template_name="bai/resumendiag_list.html"

	def get_queryset(self):
		qs = DiagRipsCons.objects.values('diagnostico__id', 'diagnostico__codigo', 'diagnostico__descripcion').annotate(cant=Count('id')).order_by('-cant')
		return qs


def georrefenciarDiagCE(request, iddiag):
	diagce = DiagRipsCons.objects.filter(~Q(ripsconsulta__paciente__lat='SD')).filter(~Q(ripsconsulta__paciente__lon='SD')).filter(Q(diagnostico__id=iddiag)).values('ripsconsulta__paciente__identificacion','ripsconsulta__paciente__lat','ripsconsulta__paciente__lon')
	some_map = folium.Map(location=[3.534089,-76.298574], zoom_start = 15)
	
	for row in diagce:
		lat = row['ripsconsulta__paciente__lat']
		lon = row['ripsconsulta__paciente__lon']
		ident = row['ripsconsulta__paciente__identificacion']
		some_map.add_child(folium.Marker(location=[lat, lon], popup=ident))

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'dignostico':diagce, 'hs':html_string}
	return redirect('bai:georref_ce')


def geolocMapaCalorDiagCE(request, iddiag):
	diagce = DiagRipsCons.objects.filter(~Q(ripsconsulta__paciente__lat='SD')).filter(~Q(ripsconsulta__paciente__lon='SD')).filter(Q(diagnostico__id=iddiag)).values('ripsconsulta__paciente__identificacion','ripsconsulta__paciente__lat','ripsconsulta__paciente__lon')
	
	some_map2 = folium.Map(location=[3.534089,-76.298574], zoom_start = 15)

	mc = MarkerCluster()


	for row in diagce:
		lat = row['ripsconsulta__paciente__lat']
		lon = row['ripsconsulta__paciente__lon']
		ident = row['ripsconsulta__paciente__identificacion']
		mc.add_child(folium.Marker(location=[lat, lon], popup=ident))

	some_map2.add_child(mc)

	filepath = 'C:/mapas/mapacalor.html'
	some_map2.save(filepath)
	webbrowser.open('file://' + filepath)
	html_string = some_map2.get_root().render()
	context = {'sm':some_map2, 'diagce':diagce, 'hs':html_string}

	return redirect('bai:georref_ce')

def mapaCalarDiagCE(request, iddiag):
	diagce = DiagRipsCons.objects.filter(~Q(ripsconsulta__paciente__lat='SD')).filter(~Q(ripsconsulta__paciente__lon='SD')).filter(Q(diagnostico__id=iddiag)).values('ripsconsulta__paciente__identificacion','ripsconsulta__paciente__lat','ripsconsulta__paciente__lon')

	m = folium.Map(location=[3.534089,-76.298574], zoom_start = 13)
	data = []
	for row in diagce:
		lat = row['ripsconsulta__paciente__lat']
		lon = row['ripsconsulta__paciente__lon']
		dato = (lat,lon)
		data.append(dato)
		

	#HeatMap.add_child(some_map3)
	HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))


	filepath = 'C:/mapas/mapacalor.html'
	m.save(filepath)
	webbrowser.open('file://' + filepath)
	html_string = m.get_root().render()
	context = {'sm':m, 'diagce':diagce, 'hs':html_string}
	return redirect('bai:georref_ce')

def listarRipsCargados(request, id):
	ripsact = RipsControl.objects.filter(id=id).first()
	cadena = ripsact.codarchivo
	if cadena.startswith('AC'):
		template = 'bai/ripsconsultaexterna_list.html'
		dfrips = RipsConsulta.objects.filter(ripscontrol_id=id)
		contexto = {'obj':dfrips}
		return render(request,template,contexto)
	if cadena.startswith('AP'):
		template = 'bai/ripsprocedimiento_list.html'
		dfrips = RipsProcedimiento.objects.filter(ripscontrol_id=id)
		contexto = {'obj':dfrips}
		return render(request,template,contexto)
	if cadena.startswith('AF'):
		template = 'bai/ripsarchivotransacciones_list.html'
		dfrips = RipsTransaccion.objects.filter(ripscontrol_id=id)
		contexto = {'obj':dfrips}
		return render(request,template,contexto)












