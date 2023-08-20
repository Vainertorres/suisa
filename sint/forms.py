from django import forms
from .models import Sintomatico


class SintomaticoForm(forms.ModelForm):
	class Meta:
		model = Sintomatico
		fields=['fecha','paciente','fiebre','cefalea','doloretrocular','mialgias','artralgias','rash',\
			'zona_endemica_dengue', 'tos','perdida_peso','sudor_nocturna','tiposintomatico','observacion']
		exclude=['um','fm','uc','fc']
		
		#widget={'nombres':forms.TextInput}
	
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
			self.fields['fecha'].widget.attrs['readonly']=True
		


