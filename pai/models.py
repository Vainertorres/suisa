from django.db import models
from django.forms import model_to_dict




# Create your models here.
from cnf.models import Ips, ClaseModelo2

class VacunaCovid(ClaseModelo2):
	fecha = models.DateField() 
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	saldovacuna = models.IntegerField()
	ingreso = models.IntegerField()
	devolucion = models.IntegerField()
	vacunadisponible = models.IntegerField()
	prograintramural = models.IntegerField()
	prograextramural = models.IntegerField()	
	dosisaplimay80intramural = models.IntegerField()
	dosisaplitrasalintramural = models.IntegerField()
	dosisaplimay80extramural = models.IntegerField()
	dosisaplitrasalextramural = models.IntegerField()
	totalintramural = models.IntegerField()
	totalextramural = models.IntegerField()
	nroequivacintramural = models.IntegerField()
	nroequivacextramural = models.IntegerField()
	nrohorahabpuntovacextra = models.FloatField()
	nrohorahabpuntovacintra = models.FloatField()
	rendihoraintramural = models.FloatField()
	rendihoraextramural = models.FloatField()
	producequipoextramural = models.FloatField()
	producequipointramural = models.FloatField()
	porcumplmetaprogintra = models.FloatField()
	porcumplmetaprogextra = models.FloatField()
	porcumpldiariointra = models.FloatField()
	porcumpldiarioextra = models.FloatField()
	nrodesespersalud = models.IntegerField()
	nrodesesmay80 = models.IntegerField()
	nroprobeventoadverso = models.IntegerField()
	nrobiolperdido = models.IntegerField()
	nrobiolperdido = models.IntegerField()
	nroesavisnotificados = models.IntegerField()
	nrodosispaiweb = models.IntegerField()


	class Meta:
		verbose_name_plural="Vacunación Covid19"

	def save(self):
		self.vacunadisponible = (self.saldovacuna + self.ingreso) - self.devolucion
		self.totalintramural = self.dosisaplimay80intramural + self.dosisaplitrasalintramural
		self.totalextramural = self.dosisaplimay80extramural + self.dosisaplitrasalextramural
		if (self.nroequivacextramural * self.nrohorahabpuntovacextra) != 0:
			self.producequipoextramural = self.totalextramural / (self.nroequivacextramural * self.nrohorahabpuntovacextra)
			self.porcumpldiarioextra = (self.totalextramural / (self.nroequivacextramural * self.nrohorahabpuntovacextra * 8))*100

		if (self.nroequivacintramural * self.nrohorahabpuntovacintra) != 0:
			self.producequipointramural = self.totalintramural / (self.nroequivacintramural * self.nrohorahabpuntovacintra)
			self.porcumpldiariointra = (self.totalintramural / (self.nroequivacintramural * self.nrohorahabpuntovacintra * 8))*100

		if self.prograextramural != 0:
			self.porcumplmetaprogextra = (self.totalextramural / self.prograextramural) * 100
		if self.prograintramural != 0:
			self.porcumplmetaprogintra = (self.totalintramural / self.prograintramural) * 100		

		super(VacunaCovid, self).save() #llamar al metodo guardar del padre

	def __str__(self):
		return "{}-{}".format(self.fecha,self.ips)

class RediarioCargado(ClaseModelo2):
	fecha = models.DateField()
	file_name = models.FileField(upload_to='rediario')
	uploaded =models.DateField(auto_now_add=True)
	activated= models.BooleanField(default=False)

	def save(self):
		#self.uc = instance.request.user
		super(RediarioCargado, self).save()

	def __str__(self):
		return f"Id del Archivo {self.id}"

class Rediario(ClaseModelo2):
	fecha = models.DateField()
	tipodoc = models.CharField(max_length=2)
	identificacion = models.CharField(max_length=20)
	fechanac = models.DateField()
	tipoedad = models.CharField(max_length=20)
	edad = models.FloatField()
	sexo = models.CharField(max_length=10)
	apellido1 = models.CharField(max_length=50)
	apellido2 = models.CharField(max_length=50, null=True, blank=True)
	nombres = models.CharField(max_length=100)
	razonsocial = models.CharField(max_length=210)
	regimen = models.CharField(max_length=50, null=True, blank=True)
	eapb = models.CharField(max_length=50, null=True, blank=True)
	departamentores = models.CharField(max_length=50, null=True, blank=True)
	municipiores = models.CharField(max_length=50, null=True, blank=True)
	area = models.CharField(max_length=30, null=True, blank=True)
	barrio = models.CharField(max_length=80, null=True, blank=True)
	direccion = models.CharField(max_length=100, null=True, blank=True)
	telefono = models.CharField(max_length=80, null=True, blank=True)
	grupoetnico = models.CharField(max_length=80, null=True, blank=True)
	desplazado = models.CharField(max_length=10, null=True, blank=True)
	discapacitado = models.CharField(max_length=20, null=True, blank=True)
	correoelectronico = models.CharField(max_length=100, null=True, blank=True)
	condiccusuaria = models.CharField(max_length=200, null=True, blank=True)
	fechaprobparto = models.DateField(null=True, blank=True)
	etapa = models.CharField(max_length=80)
	tipopoblacion = models.CharField(max_length=300)
	dosisaplicada = models.CharField(max_length=80)
	laboratorio = models.CharField(max_length=50)
	lotebiologico = models.CharField(max_length=50, null=True, blank=True)
	jeringa = models.CharField(max_length=80, null = True, blank = True)
	lotejeringa = models.CharField(max_length=50, null=True, blank=True)
	eventoadverso = models.CharField(max_length=2, default='NO', null=True, blank=True)
	vacunador = models.CharField(max_length=100, null=True, blank = True)
	municipio = models.CharField(max_length=50, null=True, blank=True)
	nombreIps = models.CharField(max_length=250)
	novedad = models.CharField(max_length=80, null=True, blank=True)
	descNovedad = models.CharField(max_length=250, null=True, blank=True)
	modalidad = models.CharField(max_length=30, null=True, blank=True)
	observacion = models.TextField(null=True, blank=True)
	reportado = models.CharField(max_length=2, null=True, blank=True)

	class Meta:
		verbose_name = 'Rediario'
		verbose_name_plural = 'Rediarios'
		ordering=['fecha']

	def save(self):
		razsoc = self.nombres
		razsoc = razsoc + " " + self.apellido1
		if self.apellido2 != "" or self.apellido2 != "0" or self.apellido2 != 0:
			pass
		else: 
			razsoc = razsoc + " " + self.apellido2

		self.razonsocial = razsoc.upper()
	
		super(Rediario, self).save()


	def __str__(self):
		return "{} - {} {} {}".format(self.fecha, self.apellido1, self.apellido2, self.nombres)

	def toJSON(self):
		item = model_to_dict(self)
		return item
		



	







	
