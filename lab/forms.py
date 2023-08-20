from django import forms 

from .models import RepLaboratorio


class RepLaboratorioForm(forms.ModelForm):
	class Meta:
		model = RepLaboratorio
		fields=['paciente','fechamuestra','muestra','redlaboratorios','tipoexamen',\
		'resultado','fecharesultado']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
		self.fields['fechamuestra'].widget.attrs['readonly'] = True
		self.fields['fecharesultado'].widget.attrs['readonly'] = True
		
