from django.forms import *
from django.forms import inlineformset_factory


from cnf.models import Paciente
from .models import MaestrobduaCargado, RepNovedad, Formularioafil, Sat, ListadoCensal, \
ContribSolidaria, PoblacionsinSisben, PoblacionEspsinLS, SIAseguramiento, PlanCobertura, \
AfilOficioSinSisben, AfilSubGrupo5SinSisben, Movilidad, SegPortabilidad, Portabilidades, \
NovLcRegTipo1, NovLcRegTipo2, NovLcRegTipo3, NovLcRegTipo4, NovLcRegTipo5, NovLcRegTipo6, \
NovLcRegTipo7, NovLcRegTipo8, NovLcRegTipo9, NovLcRegTipo10, NovLcRegTipo11, NovLcRegTipo12

class ImportFilemsForm(ModelForm):	
	class Meta:
		model=MaestrobduaCargado		
		fields=['fecha','file_name']
		exclude=['uploaded','activated','um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})

class RepNovedadForm(ModelForm):
	class Meta:
		model = RepNovedad
		fields = ['fecha','paciente','novedadbdua','eps','departamento', 'municipio', \
		'fecininovedad','valor1','valor2','valor3','valor4','valor5','valor6','valor7']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
			'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
		self.fields['fecha'].widget.attrs['readonly'] = True
		self.fields['fecininovedad'].widget.attrs['readonly'] = True

		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()

class ReportNodevadesForm(Form):
	date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class FormularioafilForm(ModelForm):
	class Meta:
		model = Formularioafil
		fields = ['fechafiliacion','paciente','tipoafiliado','aprobar','opcdesaprueba', \
		'observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechafiliacion'].widget.attrs['readonly'] = True
		
		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class SatForm(ModelForm):
	class Meta:
		model = Sat
		fields = ['fechanovedad','paciente','eps','epsdest','municipio', \
		'tiporeportesat','tipopoblacionesp','nronovedad','nivelsisben','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechanovedad'].widget.attrs['readonly'] = True
		
		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class ListadoCensalForm(ModelForm):
	class Meta:
		model = ListadoCensal
		fields = ['fechareg','paciente','municipio','tipopoblacionesp', \
		'resguardo','tipobelegiblebub','titular']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechareg'].widget.attrs['readonly'] = True
		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()

		if 'titular' in self.data:
			self.fields['titular'].queryset = Paciente.objects.all()	
		elif (self.instance.pk) and (self.instance.titular is not None):
			self.fields['titular'].queryset = Paciente.objects.all().filter(pk=self.instance.titular.pk)
		else:
			self.fields['titular'].queryset = Paciente.objects.none()


class ContribucionSolidariaForm(ModelForm):
	class Meta:
		model = ContribSolidaria
		fields = ['fechaingreso','paciente','municipio','eps','regimen', \
		'categoria','fechaliquidacion','estado','valor','atendido','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
				
		self.fields['fechaingreso'].widget.attrs['readonly'] = True
		self.fields['fechaliquidacion'].widget.attrs['readonly'] = True

		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class ContribucionSolidariaForm(ModelForm):
	class Meta:
		model = PoblacionsinSisben
		fields = ['paciente','municipio','eps','area', \
		'categoria','sisbenizado','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class PoblacionEspsinLSForm(ModelForm):
	class Meta:
		model = PoblacionEspsinLS
		fields = ['paciente','departamento','municipio','eps','area', \
		'tipopoblacionesp','modalidad','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class SIAseguramientoForm(ModelForm):
	class Meta:
		model = SIAseguramiento
		fields = ['cuentaconsi','realizacruces','bdcruces','herramientasw','responsable', \
		'cargo','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})


class PlanCoberturaForm(ModelForm):
	class Meta:
		model = PlanCobertura
		fields = ['titulo','descactividad','fechainicio','fechafin','responsable', \
		'timpodedicado','indicador','meta','resultado','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower() or field.lower() == "descactividad" or field.lower() == "meta" or field.lower() == "resultado":
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechainicio'].widget.attrs['readonly'] = True
		self.fields['fechafin'].widget.attrs['readonly'] = True
		


class AfilOficioSinSisbenForm(ModelForm):
	class Meta:
		model = AfilOficioSinSisben
		fields = ['paciente','departamento','municipio','eps','area', \
		'tipopoblacionesp','modalidad','usuarioencuestado','fechaencuesta','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechaencuesta'].widget.attrs['readonly'] = True		
		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class AfilSubGrupo5SinSisbenForm(ModelForm):
	class Meta:
		model = AfilSubGrupo5SinSisben
		fields = ['paciente','departamento','municipio','eps','area', \
		'tipopoblacionesp','modalidad','usuarioencuestado','fechaencuesta','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechaencuesta'].widget.attrs['readonly'] = True		
		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()

class MovilidadForm(ModelForm):
	class Meta:
		model = Movilidad
		fields = ['paciente','departamento','municipio','departamentosis','municipiosis','eps','regimen', \
		'nivelsisbenpe','nrofuasat','usuarioregsat','tipopoblacionesp','subgruposisbeniv',\
		'observacion','tipoafiliado', 'fechasolicitud', 'fechaefectivamov']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechasolicitud'].widget.attrs['readonly'] = True		
		self.fields['fechaefectivamov'].widget.attrs['readonly'] = True		

		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class SegPortabilidadForm(ModelForm):
	class Meta:
		model = SegPortabilidad
		fields = ['paciente','departamento','municipio','departamentodest','municipiodest', \
		'observacion','fechaatencion', 'fechasolicitud', 'fechaaplicacion','estado']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechasolicitud'].widget.attrs['readonly'] = True		
		self.fields['fechaatencion'].widget.attrs['readonly'] = True		
		self.fields['fechaaplicacion'].widget.attrs['readonly'] = True		
		

		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()


class PortabilidadForm(ModelForm):
	class Meta:
		model = Portabilidades
		fields = ['paciente','departamento','municipio','departamentodest','municipiodest', \
		'observacion','fechaatencion', 'fechasolicitud', 'fechaasignaips', \
		'ips','eps','estado']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechasolicitud'].widget.attrs['readonly'] = True		
		self.fields['fechaatencion'].widget.attrs['readonly'] = True		
		self.fields['fechaasignaips'].widget.attrs['readonly'] = True		
		

		
		if 'paciente' in self.data:
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()



class NovLcRegTipo1Form(ModelForm):
	class Meta:
		model = NovLcRegTipo1
		fields = ['tiporegistro','tipoentidad','nroidententidad','fechafinal','nrototalreg']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fechafinal'].widget.attrs['readonly'] = True		
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		
		self.fields['nrototalreg'].widget.attrs['readonly'] = True		

		

class NovLcRegTipo2Form(ModelForm):
	class Meta:
		model = NovLcRegTipo2
		fields = ['tiporegistro','tipodoc','identificacion','tipodocnew','identificacionnew', \
		'causactdocumento','fechaaplicanovedad']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "fechaaplicanovedad".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control pr"			
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})				

class NovLcRegTipo3Form(ModelForm):
	class Meta:
		model = NovLcRegTipo3
		fields = ['tiporegistro','tipodoc','identificacion','nombre1new','nombre2new']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		

class NovLcRegTipo4Form(ModelForm):
	class Meta:
		model = NovLcRegTipo4
		fields = ['tiporegistro','tipodoc','identificacion','apellido1new','apellido2new']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		


class NovLcRegTipo5Form(ModelForm):
	class Meta:
		model = NovLcRegTipo5
		fields = ['tiporegistro','tipodoc','identificacion','municipio']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		


class NovLcRegTipo6Form(ModelForm):
	class Meta:
		model = NovLcRegTipo6
		fields = ['tiporegistro','tipodoc','identificacion','tipopoblacionesp','estadolc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		

class NovLcRegTipo7Form(ModelForm):
	class Meta:
		model = NovLcRegTipo7
		fields = ['tiporegistro','tipodoc','identificacion','sexo']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		

class NovLcRegTipo8Form(ModelForm):
	class Meta:
		model = NovLcRegTipo8
		fields = ['tiporegistro','tipodoc','identificacion','fechanac']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		

class NovLcRegTipo9Form(ModelForm):
	class Meta:
		model = NovLcRegTipo9
		fields = ['tiporegistro','tipodoc','identificacion','tipopoblacionesp', 'tipobelegiblesub']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		


class NovLcRegTipo10Form(ModelForm):
	class Meta:
		model = NovLcRegTipo10
		fields = ['tiporegistro','tipodoc','identificacion','tipopoblacionesp', 'tipopoblacionespnew']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		


class NovLcRegTipo11Form(ModelForm):
	class Meta:
		model = NovLcRegTipo11
		fields = ['tiporegistro','tipodoc','identificacion','tipodoctitular', 'identificaciontitular']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		

class NovLcRegTipo12Form(ModelForm):
	class Meta:
		model = NovLcRegTipo12
		fields = ['tiporegistro','tipodoc','identificacion','tipopoblacionesp']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	
		self.fields['tiporegistro'].widget.attrs['readonly'] = True		


NovLcRegTipo2FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo2, form=NovLcRegTipo2Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo3FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo3, form=NovLcRegTipo3Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo4FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo4, form=NovLcRegTipo4Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo5FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo5, form=NovLcRegTipo5Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo6FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo6, form=NovLcRegTipo6Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo7FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo7, form=NovLcRegTipo7Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo8FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo8, form=NovLcRegTipo8Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo9FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo9, form=NovLcRegTipo9Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo10FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo10, form=NovLcRegTipo10Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo11FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo11, form=NovLcRegTipo11Form,
    extra=1, can_delete=True, can_delete_extra=True
)

NovLcRegTipo12FormSet = inlineformset_factory(
    NovLcRegTipo1, NovLcRegTipo12, form=NovLcRegTipo12Form,
    extra=1, can_delete=True, can_delete_extra=True
)