from django import forms
from .models import ImportarFile, Dengue, SegPacDengue, FilePacDengue, IecDengue, ContactoIecDen
from cnf.models import Evento
from django.db.models import Q


class ContactIecDengueForm(forms.ModelForm):
	class Meta:
		model= ContactoIecDen
		fields = ['iecdengue','nombre','edad','sexo','parentezco','eps','esqvacunacion','fiebre','dolorabdomen',
				'nauseas', 'vomito','dolorcabeza','malestargral','rash','inapetencia','doloretrocular',
				'dolormuscular', 'otrosintoma']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})

		
class IecDengueForm(forms.ModelForm):
	class Meta:
		model= IecDengue
		fields = ['dengue','fechavisita','perdxdengueips','identatiendeiec','nombreatiendeiec',
	    		'telefono','emailatiendeiec','nomips','eps','fechainisintomas','fechaconsulto',\
	    		'pacpresente','desplaotraszonas','fechadesplazo','fiebre','dolorabdomen','nauseas', \
	    		'vomito','dolorcabeza','malestargral','rash','inapetencia','doloretrocular','dolormuscular', 'otrosintoma','nroperhabitan', \
	    		'adultoenfbase','nromenoreshabitan','presenciainservibles','presenciabebederos',\
	    		'presenciaguafloreros','presenciaguavaldes','canalaguaslluvias','presenciaguatanques', \
	    		'visitafumigacion', 'nropercapacitadas','tratadosumideros','reqvisitamb',]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})
		self.fields['fechavisita'].widget.attrs['readonly'] = True
		self.fields['fechainisintomas'].widget.attrs['readonly'] = True
		self.fields['fechaconsulto'].widget.attrs['readonly'] = True
		self.fields['fechadesplazo'].widget.attrs['readonly'] = True

class FileDengueForm(forms.ModelForm):
	class Meta:
		model = FilePacDengue
		fields = ['dengue','descripcion','archivo']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})

class ImportFileForm(forms.ModelForm):
	evento = forms.ModelChoiceField(queryset=Evento.objects.filter(Q(codigo=210) | Q(codigo=220) | Q(codigo=580)))	
	class Meta:
		model=ImportarFile		
		fields=['semepidemiologica','evento','file_name']
		exclude=['uploaded','activated','um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})

class DengueForm(forms.ModelForm):
	class Meta:
		model = Dengue
		fields = ['fec_not','semana', 'paciente','edad','umedad','telefono', 'evento']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
			'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

class SegPacDengueForm(forms.ModelForm):
	class Meta:
		model = SegPacDengue
		fields=['dengue','fecha','hallazgos','segsaludambiental','ctrllarvario','fumigacion','educacion','entregatoldillos',\
		'cantolperiesgo','cantolcoomorb','cantoladulmay','cantolmencinco','cantolembarazadas']
		exclude=['um','fm','uc','fc']

	def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs) #para que se inicialice
			for field in iter(self.fields):
				self.fields[field].widget.attrs.update({				
					'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
			self.fields['fecha'].widget.attrs['readonly'] = True



