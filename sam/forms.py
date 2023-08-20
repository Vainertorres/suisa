from django import forms

from .models import Propietario, Establecimiento, ActaEstabEducativo, ItemActaEstabEducativo, Atiende_ActaEstabEduc, \
ActaEstEduFuncionario, Atiende_ActaEstabEduc



class PropietarioForm(forms.ModelForm):
	class Meta:
		model = Propietario
		fields = ['tipodoc','nitcc','nombres','apellido1','apellido2','telfijo','telcelular', \
		'correoelectronico']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})


class EstablecimientoForm(forms.ModelForm):
	class Meta:
		model = Establecimiento
		fields = ['nitcc','razonsocial','nroinscripcion','nombrecomercial','direccion','telefono', \
		'fax', 'nromatricula', 'departamento', 'municipio', 'lugarubica', 'correoelectronico', \
		'propietario', 'replegal', 'direccionotifica', 'dptonotifica', 'mpionotifica', \
		'horariofunciona', 'nrotrabajadores']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

class ActaEstabEducativoForm(forms.ModelForm):
	class Meta:
		model = ActaEstabEducativo
		fields=['fecha','nroacta','ciudad','establecimiento','nombrerector','tipodocrector','identificacionrector', \
		'nroestjormanhombres','nroestjormanmujeres','nroestjortarhombres','nroestjortarmujeres','nroestjornochombres', \
		'nroestjornocmujeres','nrodocenteshombres','nrodocentesmujeres','nroaulas','nropatios','nrocafeterias', \
		'fechaultinspeccion','nroactaultinspeccion','ultconcepto','motivoVisita','concepto']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

class ItemActaEstabEducativoForm(forms.ModelForm):
	class Meta:
		model = ItemActaEstabEducativo
		fields = ['pregunta','evaluacion','hallazgos','habilitada']

	def __init__(self, *args, **kwargs):		
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "pregunta".lower():
				self.fields[field].widget.attrs.update({				
					'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
					'rows':"1",				
					'readonly':True,
					'enable':False
					})
				
			else:
				if field.lower() == "hallazgos".lower():
					self.fields[field].widget.attrs.update({				
					'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
					'rows':"1",				
					})
				else:
					self.fields[field].widget.attrs.update({				
					'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
					})

			 


class ActaEstEduFuncionarioForm(forms.ModelForm):
	class Meta:
		model = ActaEstEduFuncionario
		fields=['funcionario']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})


class Atiende_ActaEstabEducForm(forms.ModelForm):
	class Meta:
		model= Atiende_ActaEstabEduc
		fields=['tipodoc','identificacion','nombre','institucion','cargo']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
