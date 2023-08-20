from django.db import models
from django.contrib.auth.models import User
from cnf.models import ClaseModelo, ClaseModelo2, Sexo
# Create your models here.

from cnf.models import Paciente, Evento, UmEdad, Ocupacion, Regimen, Eps, Departamento, Municipio, \
ClasiFinicial, Upgd, SemEpidemiologica, Evento, Parentezco


class Conducta(ClaseModelo):
	codigo=models.IntegerField()
	descripcion= models.CharField(max_length=80)

	class Meta:
		verbose_name_plural = "Conductas" 

	def __str__(self):
		return "{}".format(self.descripcion)

class ClasiFinalDen(ClaseModelo):
	codigo=models.IntegerField()
	descripcion=models.CharField(max_length=80)

	class Meta:
		verbose_name_plural = 'Clasificación Final Dengue'

	def __str__(self):
		return "{}".format(self.descripcion)

class ImportarFile(ClaseModelo2):
	semepidemiologica = models.ForeignKey(SemEpidemiologica, on_delete=models.CASCADE)
	evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
	file_name = models.FileField(upload_to='den')
	uploaded =models.DateField(auto_now_add=True)
	activated= models.BooleanField(default=False)

	def save(self):
		#self.uc = instance.request.user
		super(ImportarFile, self).save()

	def __str__(self):
		return f"Id del Archivo {self.id}"

class Dengue(ClaseModelo):
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
	Departamentor = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
	municipior = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
	fec_con = models.DateField(null=True, blank=True)
	ini_sin = models.DateField(null=True, blank=True)
	clasiFinicial = models.ForeignKey(ClasiFinicial, on_delete=models.CASCADE, null=True, blank=True)
	pac_hos = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	fec_hos = models.DateField(null=True, blank=True)
	clasifinalden = models.ForeignKey(ClasiFinalDen, on_delete=models.CASCADE, null=True, blank=True)
	telefono = models.CharField(max_length=30, null=True, blank=True)
	nit_upgd = models.CharField(max_length=30, null=True, blank=True)
	upgd = models.ForeignKey(Upgd, on_delete=models.CASCADE, null=True, blank=True)
	fiebre = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	cefalea = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	dolrretroo = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	mialgias = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	artralgia = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	erupcionr = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	dolor_abdo = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	vomito = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	diarrea = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	somnolenci = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	hipotensio = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	hepatomeg = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	hem_mucosa = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	hipotermia = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	aum_hemato = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	caida_plaq = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	acum_liqui = models.CharField(max_length=1, choices=SINO, null=True, blank=True) 
	extravasac = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	hemorr_hem = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	choque = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	danio_organ = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	muesttejid = models.CharField(max_length=1, choices=SINO, null=True, blank=True)
	conducta = models.ForeignKey(Conducta, on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		verbose_name_plural="Notificación Dengue - 210"


	def __str__(self):
		return "{} {} {} - {}".format(self.fec_not, self.semana ,self.evento.descripcion, self.paciente)

class SegPacDengue(ClaseModelo):
	SINO = (
        ('1', 'Si'),
        ('2', 'No'),
    )
	dengue = models.ForeignKey(Dengue, on_delete=models.CASCADE)
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
	segsaludambiental = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural="Seguimientos"

	def __str__(self):
		return "{} - {}".format(self.dengue - self.hallazgos)


class FilePacDengue(ClaseModelo2):
	dengue = models.ForeignKey(Dengue, on_delete=models.CASCADE)
	descripcion = models.CharField(max_length=150)
	archivo = models.FileField(upload_to='den/miarchivo/', null=True, blank=True)

	class Meta:
		verbose_name_plural="Archivos Dengue"

	def __str__(self):
		return "{} - {}".format(self.descripcion, self.descripcion)


class IecDengue(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
	dengue = models.ForeignKey(Dengue, on_delete=models.CASCADE)
	fechavisita = models.DateField()
	perdxdengueips = models.CharField(max_length=2, choices=SINO, null=True, blank=True, default="SI")
	identatiendeiec = models.CharField(max_length=20)
	nombreatiendeiec = models.CharField(max_length=100)
	telefono = models.CharField(max_length=50, null = True, blank=True)
	emailatiendeiec = models.CharField(max_length=50, null=True, blank=True)
	nomips = models.CharField(max_length=100, null=True, blank=True)
	eps=models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	fechainisintomas = models.DateField(null=True, blank=True)
	fechaconsulto = models.DateField(null=True, blank=True)
	pacpresente=  models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	desplaotraszonas = models.CharField(max_length=100, null=True, blank = True)
	fechadesplazo = models.DateField(null=True, blank=True)
	fiebre = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dolorabdomen = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	nauseas = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	vomito = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dolorcabeza = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	malestargral = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	rash = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	inapetencia = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	doloretrocular = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dolormuscular = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	otrosintoma = models.CharField(max_length=100, null=True, blank=True)
	nroperhabitan = models.IntegerField()
	adultoenfbase = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	nromenoreshabitan = models.IntegerField()
	presenciainservibles = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	presenciabebederos = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	presenciaguafloreros = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	presenciaguavaldes = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	canalaguaslluvias = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	presenciaguatanques = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	visitafumigacion = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	nropercapacitadas = models.IntegerField()
	tratadosumideros = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	reqvisitamb = models.BooleanField(default=False)

	class Meta:
		verbose_name='IEC Dengue'

	def __str__(self):
		return "{}".format(self.dengue)

class ContactoIecDen(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
	iecdengue = models.ForeignKey(IecDengue, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=100)
	edad = models.IntegerField(null=True, blank=True)
	sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE)
	parentezco = models.ForeignKey(Parentezco, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete = models.CASCADE)
	esqvacunacion = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	fiebre = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dolorabdomen = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	nauseas = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	vomito = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dolorcabeza = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	malestargral = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	rash = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	inapetencia = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	doloretrocular = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	dolormuscular = models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	otrosintoma = models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		verbose_name='Contactos Pac. Dengue'

	def __str__(self):
		return "{}".format(nombre) 





















	

	











	


