from django import forms
from .models import ImportarCie10, PeriodoImportRips, Diagnosticos

class PeriodoImportRipsForm(forms.ModelForm):
	
	class Meta:
		model= PeriodoImportRips
		fields=['ips','fecharemision','fileCT','fileUS','fileAC','fileAP','fileAU', \
		 'fileAH', 'fileAM', 'fileAF', 'fileAT']
		exclude=['activated','um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
		self.fields['fecharemision'].widget.attrs['readonly'] = True


class ImportCie10Form(forms.ModelForm):
	class Meta:
		model=ImportarCie10
		fields=['file_name','file_cups', 'file_cums']
		exclude=['uploaded','activated','um','uc','fm','fc']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})


class DiagnosticosForm(forms.ModelForm):
	class Meta:
		model = Diagnosticos
		exclude = ['uploaded','activated','um','uc','fm','fc']
		fields=['codigo','descripcion','notifobligatoria','idcapitulo', 'capitulo','codcie3','descripcie3']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

		