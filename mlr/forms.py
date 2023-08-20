from django import forms
from .models import Malaria, ImportarMalaria, SegPacMalaria, Conglomerado, ConglomeradoMalaria, \
SegCongloMalaria, FileConglomerado
from cnf.models import Evento


class FileConglomeradoForm(forms.ModelForm):
	class Meta:
		model = FileConglomerado
		fields = ['conglomerado','descripcion','archivo']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})


class PacienteCongloMalariaForm(forms.ModelForm):
	class Meta:
		model= ConglomeradoMalaria
		fields = ['conglomerado','malaria']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

class ConglomeradoMalariaForm(forms.ModelForm):
	class Meta:
		model= Conglomerado
		fields = ['fechainibrote','descripcion','barrio','visitado','fechavisita','nrodecasos']
		exclude=['um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice

		for field in iter(self.fields):
			if field.lower() == "descripcion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
			
		self.fields['fechainibrote'].widget.attrs['readonly'] = True
		self.fields['fechavisita'].widget.attrs['readonly'] = True

class ImportFileForm(forms.ModelForm):
	evento = forms.ModelChoiceField(queryset=Evento.objects.filter(codigo=465))

	class Meta:
		model= ImportarMalaria
		fields = ['semepidemiologica','evento','file_name']
		exclude=['uploaded','activated','um','uc','fm','fc']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice



		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

		


class MalariaForm(forms.ModelForm):
	class Meta:
		model= Malaria
		fields = ['fec_not','semana', 'paciente','edad','umedad','telefono', 'evento','tratamiento', \
		'especieinf','tipoexamen','complicaci','com_cerebr','com_renal','com_hepati','com_pulmon','com_hemato',\
		'com_otras']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})


class SegPacMalariaForm(forms.ModelForm):
	class Meta:
		model = SegPacMalaria
		fields=['malaria','fecha','hallazgos','ctrllarvario','fumigacion','educacion','entregatoldillos',\
		'cantolperiesgo','cantolcoomorb','cantoladulmay','cantolmencinco','cantolembarazadas']
		exclude=['um','fm','uc','fc']

	def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs) #para que se inicialice
			for field in iter(self.fields):
				self.fields[field].widget.attrs.update({				
					'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
			self.fields['fecha'].widget.attrs['readonly'] = True


class SegConglomeradoMalariaForm(forms.ModelForm):
	class Meta:
		model = SegCongloMalaria
		fields=['conglomerado','fecha','hallazgos','ctrllarvario','fumigacion','educacion','entregatoldillos',\
		'cantolperiesgo','cantolcoomorb','cantoladulmay','cantolmencinco','cantolembarazadas']
		exclude=['um','fm','uc','fc']

	def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs) #para que se inicialice
			for field in iter(self.fields):
				if field.lower() == "hallazgos".lower():
					self.fields[field].widget.attrs.update({				
					'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
					'rows':"4"
					})
				else:
					self.fields[field].widget.attrs.update({				
					'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
					})
			self.fields['fecha'].widget.attrs['readonly'] = True




