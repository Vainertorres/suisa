from django import forms

from .models import MaestrobduaCargado

class ImportFilemsForm(forms.ModelForm):	
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

