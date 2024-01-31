from django import forms 
from .models import Bac, Fichaiec, Antecedenteviaje, SegFichaIec, Conglomerado, ImportSivCvdFile, \
Notif_covid, AntecHospitalizacion, FileFichaIec, ContactosIec, DesplazaContacto, SegContacto, \
NotifPaConglomerado, ContactoAislado, SegContactoAislado, ConfigConglomerado, Segnotifcovid

from cnf.models import Paciente


class ConfigConglomeradoForm(forms.ModelForm):
	class Meta:
		model = ConfigConglomerado
		fields=['conglomerado','consecutivo','descripcion','descmedidasinstitucion',\
		'descmeorgasalud','fichaiec','barrio','estadoconglomerado','nrocasospos', 'nrocasosneg',\
		'nrocasospendiente','totalperaislados','fuente','causacontagio','nrocasosrelacionados', \
		'medidascorrectivas','controlado']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "descripcion".lower() or field.lower() == "descmedidasinstitucion".lower() or \
			field.lower() == "descmeorgasalud".lower() or field.lower() == "medidascorrectivas".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})



class SegContactoAisladoForm(forms.ModelForm):
	class Meta:
		model = SegContactoAislado
		fields=['contactoaislado','fecha','sintomas','tos','Fiebre','odinofagia','dificultadrespirar', \
		'fatiga','hospitalizado','observacion','funcionario']


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
		self.fields['fecha'].widget.attrs['readonly'] = True
		


class ContactoAisladoForm(forms.ModelForm):
	class Meta:
		model = ContactoAislado
		fields=['notifPaConglomerado','paciente','edad','cargo','municipio','eps','feciniaislamiento', \
		'fechafinaislamiento','valmedicagral','motivo','diasaislamiento','aislaconincapacidad',\
		'requiereprueba','fechatomamuestra','resultado','descripcion']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "motivo".lower() or field.lower() == "descripcion".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['feciniaislamiento'].widget.attrs['readonly'] = True
		self.fields['fechafinaislamiento'].widget.attrs['readonly'] = True
		self.fields['fechatomamuestra'].widget.attrs['readonly'] = True
		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()
		



class NotifPaConglomeradoForm(forms.ModelForm):
	class Meta:
		model = NotifPaConglomerado
		fields=['conglomerado','paciente','edad','municipio','eps','fecinisintomas','fechatomamuestra',\
		'resultado','descripcion','observacion']


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observacion".lower() or field.lower() == "descripcion".lower() :
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		self.fields['fecinisintomas'].widget.attrs['readonly'] = True
		self.fields['fechatomamuestra'].widget.attrs['readonly'] = True
		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()
		


class SeguimientoContactoForm(forms.ModelForm):
	class Meta:
		model = SegContacto
		fields=['contactosiec','sintomatico','fecha','tos','fiebre','odinofagia','difrespirar',\
		'adinamia','hospitalizado']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
		self.fields['fecha'].widget.attrs['readonly'] = True


class DesplazaContactoForm(forms.ModelForm):
	class Meta:
		model = DesplazaContacto
		fields=['contactosiec','pais','departamento','ciudad'] 

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

class ContactosForm(forms.ModelForm):
	class Meta:
		model = ContactosIec
		fields = ['fichaiec','paciente','edad','umedad','clasecontacto','fechaposexpo', \
		'institucionsalud','sintomatico','fechainisintomas','hospitalizado','fechamuestra',\
		'resultmxcovid']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
		self.fields['fechaposexpo'].widget.attrs['readonly'] = True
		self.fields['fechamuestra'].widget.attrs['readonly'] = True
		self.fields['fechainisintomas'].widget.attrs['readonly'] = True

		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()
		


class FileIecForm(forms.ModelForm):
	class Meta:
		model = FileFichaIec
		fields = ['fichaiec','descripcion','archivo']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})

class NotifCovidForm(forms.ModelForm):
	class Meta:
		model= Notif_covid
		fields=['fec_not','evento','paciente', 'semana','upgd','tos','fiebre','odinofagia','dif_res',\
		'adinamia','vac_ei','dos_ei','asma','epoc','diabetes','vih','enf_card','cancer','obesidad','ins_renal',\
		'otr_medinm','fumador', 'tuberculos','otros_dc','cual_ot_dc','uso_antiv','fec_antiv','serv_hosp','fec_inguci', \
		'miocarditi', 'septicemia', 'falla_resp','otros_sint','dol_gar','rinorrea','conjuntivi','cefalea','diarrea','rx_torax','fec_tom_ra']
		exclude=['um','uc','fm','fc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'readonly' : "True"
			})
		if 'paciente' in self.data:
			idpac = self.data['paciente']	
			print(idpac)		
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()

class SegNotifCovidForm(forms.ModelForm):
	class Meta:
		model= Segnotifcovid
		fields=['notifcovid','fecha','hallazgo','proxseg','fecproxseg','fileseg']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "hallazgo".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})
		

class ImportFileCvdForm(forms.ModelForm):
	class Meta:
		model=ImportSivCvdFile
		fields=['semepidemiologica','evento','file_name']
		exclude=['uploaded','activated','um','uc','fm','fc']

class BacForm(forms.ModelForm):
	class Meta:
		model = Bac
		fields=['fecharealiza','paciente', 'edad', 'umedad', 'grupopob', 'riesgopsicosoc', 'eps', \
		'tos','dificultadrespirar','dolorgarganta', 'fiebre', 'sano','diabetes','enfcardiaca','cancer',\
		'enfrenal', 'trata_corticoides','asma_epoc','malnutricion','otracoomorbilidad','temperatura',\
		'prueba_olfato','sospechoso','pruebacovid', 'fichaepidemiologica', 'resultado', 'observaciones']
		exclude=['um','fm','uc','fc']
		#widget={'nombres':forms.TextInput}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if field.lower() == "observaciones".lower():
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})

		if 'paciente' in self.data:
			idpac = self.data['paciente']			
			self.fields['paciente'].queryset = Paciente.objects.all()	
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()
		

class FichaiecForm(forms.ModelForm):


	#ambitoatencion = forms.ForeignKeyField(required=True)

	class Meta:
		model = Fichaiec
		fields=['fecha','paciente','fecinisintomas','desplazamientos','contact_pac','lugarcontact','antinflamatorios','fiebre','tos','dificultadrespirar', \
		'taquipnea','dolorgarganta','escalofrios','nauseas','vomito','dolor_torax','mialgia','diarrea','dolor_abdominal', \
		'dolor_cabeza','malestar_general','otro','cualotro','asma','epoc','trastorno_neuro', 'inmunosupresion','enfrenal', \
		'enfcardiaca','enfhematologica','diabetes','obesidad','enfhepatica','embarazo','semgestacion','tabaquismo',\
		'alcoholismo','trastorno_reumatologico','fechaprimuestra','muestra','cualotramuestra','resfilarray','respcr', \
		'fechareslab', 'anamnesis','nomapentrevistador','telentrevistador','departamento','municipio','estadoiec','fechaegreso',\
		'ambitoatencion']
		exclude=['um','fm','uc','fc']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})
		self.fields['fecha'].widget.attrs['readonly'] = True
		self.fields['fecinisintomas'].widget.attrs['readonly'] = True
		self.fields['fechaprimuestra'].widget.attrs['readonly'] = True
		self.fields['fechareslab'].widget.attrs['readonly'] = True
		self.fields['fechaegreso'].widget.attrs['readonly'] = True
		
		if 'paciente' in self.data:
			idpac = self.data['paciente']
			self.fields['paciente'].queryset = Paciente.objects.all()
		elif self.instance.pk:
			self.fields['paciente'].queryset = Paciente.objects.all().filter(pk=self.instance.paciente.pk)
		else:
			self.fields['paciente'].queryset = Paciente.objects.none()
		

class AntViajeForm(forms.ModelForm):
	fechaini = forms.DateInput()
	fechafin = forms.DateInput()
	class Meta:
		model = Antecedenteviaje
		fields=['fichaiec','pais','ciudad','fechaini','fechafin']
		exclude=['um','fm','uc','fc']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})		
		self.fields['fechaini'].widget.attrs['readonly'] = True
		self.fields['fechafin'].widget.attrs['readonly'] = True

class SegFichaIecForm(forms.ModelForm):
	class Meta:
		model = SegFichaIec
		fields=['fecha', 'fichaiec','hallazgo','tipocontacto','estadoafectacion','pendiente','fechaprog','descpendiente',\
		'ambitoatencion', 'resprapida','fiebremasdosdias','pechosuena','somnolencia','ataqueconvulsion',\
		'decaimiento','deteriorogeneral','dificultadrespirar', 'resultadopcvd','fechaultprueba',\
		'nombreinforma','cargoactividadinfo','telfijoinfo','celularinfo','emailinfo']
		exclude=['um','fm','uc','fc']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			if (field.lower() == "descpendiente".lower()) or (field.lower() == "hallazgo".lower()):
				self.fields[field].widget.attrs.update({				
				'class':"form-control", #colocar la clase de bootsTrap a todos los controles o campos
				'rows':"3"
				})
			else:
				self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
				})	
		self.fields['fecha'].widget.attrs['readonly'] = True
		self.fields['fechaprog'].widget.attrs['readonly'] = True
		self.fields['fechaultprueba'].widget.attrs['readonly'] = True

class ConglomeradoForm(forms.ModelForm):
	class Meta:
		model = Conglomerado
		fields=['tipoconglomerado', 'descripcion','nomreplegal','direccion','telcontacto','lat','lon']
		exclude=['um','fm','uc','fc']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})	

class AntHospitalizacionForm(forms.ModelForm):
	fechaconsulta = forms.DateInput()	
	class Meta:
		model = AntecHospitalizacion
		fields=['fichaiec','fechaconsulta','institucionsalud','observacion']
		exclude=['um','fm','uc','fc']
		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs) #para que se inicialice
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({				
				'class':"form-control" #colocar la clase de bootsTrap a todos los controles o campos
			})		
		self.fields['fechaconsulta'].widget.attrs['readonly'] = True
		