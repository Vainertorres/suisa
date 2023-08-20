from django.db import models

# Create your models here.

from cnf.models import ClaseModelo2, Paciente,Evento, UmEdad, Ocupacion, Regimen, Eps, Departamento,\
Municipio, ClasiFinicial, Upgd, CondiccionFinal, SemEpidemiologica, Fuente, Pais, Barrio

from bai.models import Diagnosticos

from lab.models import TipoExamen

class EspecieInf(ClaseModelo2):
	codigo = models.IntegerField()
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Especie Infectante'

	def __str__(self):
		return "{}".format(self.descripcion)

class Tratamiento(ClaseModelo2):
	codigo = models.IntegerField()
	descripcion = models.CharField(max_length=100)

	class Meta:
		verbose_name='Tratamientos de Malaria'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)


class Malaria(ClaseModelo2):
	TRIMESTREGES=(
    	('1','Primer trimestre'),
    	('2','Segundo trimestre'),
    	('3','Tercer trimestre'),
    )
	SINO = (
        ('1', 'Si'),
        ('2', 'No'),
    )
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)
	evento=models.ForeignKey(Evento, on_delete=models.CASCADE)
	fec_not = models.DateField()
	semana = models.IntegerField()
	anio = models.IntegerField()
	cod_pre = models.CharField(max_length=20)
	cod_sub = models.CharField(max_length=2)
	edad = models.IntegerField()
	umedad = models.ForeignKey(UmEdad, on_delete=models.CASCADE, null=True, blank=True)
	ocupacion = models.ForeignKey(Ocupacion, on_delete=models.CASCADE, null=True, blank=True)
	regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	estrato = models.IntegerField(null=True, blank=True)
	gp_discapa = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_desplaz = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_migrant = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_carcela = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_gestan = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	sem_ges = models.IntegerField(null=True, blank=True) 
	gp_indigen = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_pobicbf = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_mad_com = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_desmovi = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_psiquia = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_vic_vio = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	gp_otros = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fuente = models.ForeignKey(Fuente, on_delete=models.CASCADE, null=True, blank=True)
	paisr = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, blank=True)
	departamentor = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
	municipior = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
	fec_con = models.DateField(null=True, blank=True)
	ini_sin = models.DateField(null=True, blank=True)
	clasiFinicial = models.ForeignKey(ClasiFinicial, on_delete=models.CASCADE, null=True, blank=True)
	pac_hos = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fec_hos = models.DateField(null=True, blank=True)		
	condiccionfinal = models.ForeignKey(CondiccionFinal, on_delete=models.CASCADE, null=True, blank=True)
	fec_def = models.DateField(null=True, blank=True)
	ajuste = models.CharField(max_length=10, null=True, blank=True)
	fec_ajuste = models.DateField(null=True, blank=True)
	cer_def = models.CharField(max_length=50, null=True, blank=True)
	cbmte = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE, null=True, blank=True)
	telefono = models.CharField(max_length=30, null=True, blank=True)
	nit_upgd = models.CharField(max_length=30, null=True, blank=True)
	upgd = models.ForeignKey(Upgd, on_delete=models.CASCADE, null=True, blank=True)
	vig_activa = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	sintomatic = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	clas_caso = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	recrudece = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 	
	trimestre = models.CharField(max_length=1, choices=TRIMESTREGES, null=True, blank=True) 
	tipoexamen = models.ForeignKey(TipoExamen, on_delete=models.CASCADE, null=True, blank=True) 	
	recuento = models.FloatField(null=True, blank=True, default=0)
	gametocito = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 	
	desplazami = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 	
	despla_codpais = models.IntegerField(null=True, blank=True)
	despla_coddep = models.IntegerField(null=True, blank=True)
	despla_codmun = models.IntegerField(null=True, blank=True)
	complicaci = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	com_cerebr = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	com_renal = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	com_hepati = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	com_pulmon = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	com_hemato = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	com_otras = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, null=True, blank=True)
	f_ini_trat = models.DateField(null=True, blank=True)
	especieinf =  models.ForeignKey(EspecieInf, on_delete=models.CASCADE, null=True, blank=True) 
	resp_diag = models.CharField(max_length=150, null=True, blank=True)
	fec_result = models.DateField(null=True, blank=True)
	result_exa = models.CharField(max_length=100, null=True, blank=True)
	nuevo = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	nom_upgd = models.CharField(max_length=150, null=True, blank=True) 
	npais_proce = models.IntegerField(null=True, blank=True)
	ndep_proce = models.IntegerField(null=True, blank=True)
	nmun_proce = models.IntegerField(null=True, blank=True)
	

	class Meta:
		verbose_name_plural="Notificación Casos de Malaria - 465"

	def __str__(self):
		return "{} - Notificado el: {} Sem: {} Evento: {}".format( self.paciente, self.fec_not, self.semana ,self.evento.descripcion,)


class ImportarMalaria(ClaseModelo2):
	semepidemiologica = models.ForeignKey(SemEpidemiologica, on_delete=models.CASCADE)
	evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
	file_name = models.FileField(upload_to='mlr')
	uploaded =models.DateField(auto_now_add=True)
	activated= models.BooleanField(default=False)

	def save(self):
		#self.uc = instance.request.user
		super(ImportarMalaria, self).save()

	def __str__(self):
		return f"Id del Archivo {self.id}"

class SegPacMalaria(ClaseModelo2):
	SINO = (
        ('1', 'Si'),
        ('2', 'No'),
    )
	malaria = models.ForeignKey(Malaria, on_delete=models.CASCADE)
	fecha= models.DateField()
	hallazgos = models.TextField()
	ctrllarvario = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	fumigacion = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	educacion = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	entregatoldillos = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	cantolperiesgo = models.IntegerField(default=0)
	cantolcoomorb = models.IntegerField(default=0)
	cantoladulmay = models.IntegerField(default=0)
	cantolmencinco = models.IntegerField(default=0)
	cantolembarazadas = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural="Seguimientos Malaria"

	def __str__(self):
		return "{} - {}".format(self.malaria - self.hallazgos)

class Conglomerado(ClaseModelo2):		
	fechainibrote = models.DateField()
	descripcion = models.TextField()
	barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, null=True, blank=True)		
	visitado=models.BooleanField(default=False)
	fechavisita = models.DateField(null=True, blank=True)
	nrodecasos=models.IntegerField(null=True, blank=True)

	class Meta:
		verbose_name='Conglomerado de Casos de Malaria'
		ordering=['fechainibrote']

	def __str__(self):
		return "Fecha Brote:{}, Lugar: {}. Nro de casos: {} ".format(self.fechainibrote, self.barrio, self.nrodecasos)


class ConglomeradoMalaria(ClaseModelo2):
	conglomerado = models.ForeignKey(Conglomerado, on_delete=models.CASCADE)
	malaria = models.ForeignKey(Malaria, on_delete=models.CASCADE)

	class Meta:
		verbose_name='Casos de Malaria en Conglomerado'

	def __str__(self):
		return "Conglomerado: {} - Paciente: {}".format(self.conglomerado, self.malaria)


class SegCongloMalaria(ClaseModelo2):
	SINO = (
        ('1', 'Si'),
        ('2', 'No'),
    )
	conglomerado = models.ForeignKey(Conglomerado, on_delete=models.CASCADE)
	fecha= models.DateField()
	hallazgos = models.TextField()
	ctrllarvario = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	fumigacion = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	educacion = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	entregatoldillos = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	cantolperiesgo = models.IntegerField(default=0)
	cantolcoomorb = models.IntegerField(default=0)
	cantoladulmay = models.IntegerField(default=0)
	cantolmencinco = models.IntegerField(default=0)
	cantolembarazadas = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural="Seguimientos Conglomerado Malaria"

	def __str__(self):
		return "{} - {}".format(self.conglomerado - self.hallazgos)

class FileConglomerado(ClaseModelo2):		
	conglomerado = models.ForeignKey(Conglomerado, on_delete=models.CASCADE)
	descripcion = models.CharField(max_length=200)
	archivo = models.FileField(upload_to='mlr', null=True, blank=True)

	class Meta:
		verbose_name='Archivos Adjuntos Conglomerado'
		ordering = ['descripcion']

