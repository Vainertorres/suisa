from django import forms

from .models import RediarioCargado, Rediario, RediarioPaiRegCargado

class ImportFileForm(forms.ModelForm):	
	class Meta:
		model=RediarioCargado		
		fields=['fecha','file_name']
		exclude=['uploaded','activated','um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})

class ImportFilePaiRegForm(forms.ModelForm):	
	class Meta:
		model=RediarioPaiRegCargado		
		fields=['fecha','periodo','file_name', 'ips']
		exclude=['uploaded','activated','um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
			})

class RediarioCreateForm(forms.ModelForm):	
	class Meta:
		model=Rediario			
		exclude=['um','uc','fm','fc','razonsocial', 'reportado', 'estado']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == 'observacion'.lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"2"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				
				})
