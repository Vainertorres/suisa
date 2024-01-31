import time

#from django import forms 
from django.forms import *
from django.forms import inlineformset_factory

from cnf.models import Paciente
from .models import Pqrs, SeguimientoPQRS


class PqrsForm(ModelForm):
	
	class Meta:
		model = Pqrs
		fields=['fecha','paciente','edad','victima','desplazado','pqrscontra', \
		'resolinmediata','eps','ips','otrainstobjetoqueja','periodoresolucion', \
		'iniciaderepeticion','iniciatutela', 'explicacion', 'terderepeticion', \
		'tertutela','serviciosobjqueja','respondida','tiporespuestapqrs','fecharespuesta']
			
		exclude=['um','fm','uc','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "explicacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"4"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})

		self.fields['fecha'].widget.attrs['readonly'] = True
		
		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=idpac)	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()

class SeguimientoPqrsForm(ModelForm):
	class Meta:
		model=SeguimientoPQRS
		fields=['fecha','observacion']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in iter(self.fields):
			if field.lower() == "observacion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control pr" #colocar la clase de bootsTrap a todos los controles o campos
				})
		#self.fields['fecha'].widget.attrs['readonly'] = True

SegPqrsFormSet = inlineformset_factory(
    Pqrs, SeguimientoPQRS, form=SeguimientoPqrsForm,
    extra=1, can_delete=True, can_delete_extra=True
)

class ReportPqrsForm(Form):
	date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

		
			
		