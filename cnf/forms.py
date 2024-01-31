from django import forms
from .models import Paciente, Barrio

class PacienteForm(forms.ModelForm): 
	class Meta:
		model = Paciente
		fields=['tipodoc', 'identificacion','nombre1','nombre2','apellido1','apellido2','fechanac',\
		'departamento','municipio','direccion','telefono','correoelectronico', 'barrio','area',\
		'regimen','eps','sexo', 'etnia','lat', 'lon', 'pais']
		exclude=['um','fm','uc','fc']
		

	def __init__(self, *args, **kwargs):
  		super().__init__(*args, **kwargs) #para que se inicialice
  		for field in iter(self.fields):
  			self.fields[field].widget.attrs.update({
               'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
        	})
  		self.fields['fechanac'].widget.attrs['readonly'] = True
  		

