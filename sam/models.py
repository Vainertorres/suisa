from django.db import models

# Create your models here.

from cnf.models import ClaseModelo2, Tipodoc, Departamento, Municipio, Funcionario

class Concepto(ClaseModelo2):
	idconcepto = models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=30)
	porcumplemin = models.FloatField()
	porcumplemax = models.FloatField()

	class Meta:
		verbose_name_plural="Conceptos Sanitarios"

	def __str__(self):
		return "{}".format(self.descripcion)

class Evaluacion(ClaseModelo2):
	idevaluacion = models.CharField(max_length=2)
	descripcion = models.CharField(max_length=50)
	nota = models.CharField(max_length=200, null=True, blank=True)

	class Meta:
		verbose_name_plural = "Evaluaciones"

	def __str__(self):
		return "{}".format(self.descripcion)

class LugarUbica(ClaseModelo2):
	idlugarubica = models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural="Lugares donde se ubica el Establecimiento"

	def __str__(self):
		return "{}".format(self.descripcion)

class MotivoVisita(ClaseModelo2):
	idmotivovisita = models.CharField(max_length=3)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name_plural="Motivos de Visita"

	def __str__(self):
		return "{}".format(self.descripcion)

class Propietario(ClaseModelo2):
	tipodoc = models.ForeignKey(Tipodoc, on_delete=models.CASCADE)
	nitcc = models.CharField(max_length=30)
	nombres = models.CharField(max_length=80)
	apellido1 = models.CharField(max_length=40)
	apellido2 = models.CharField(max_length=40, null=True, blank=True)
	telfijo = models.CharField(max_length=20, null=True, blank=True)
	telcelular = models.CharField(max_length=30, null=True, blank=True)
	correoelectronico = models.EmailField(max_length=200, null=True, blank=True)

	class Meta:
		verbose_name_plural='Propietarios'

	def __str__(self):
		razsoc = self.nombres + " " + self.apellido1
		if not (self.apellido2 == "" or self.apellido2==None):
			razsoc += " " + self.apellido2

		return "{} : {}".format(self.nitcc, razsoc)

class TipoActa(ClaseModelo2):
	idtipoacta = models.CharField(max_length=15, unique=True)
	descripcion = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural="Tipos de Actas"

	def __str__(self):
		return "{}".format(self.descripcion)


class Bloque(ClaseModelo2):
	tipoacta = models.ForeignKey(TipoActa, on_delete=models.CASCADE)
	idbloque = models.IntegerField()
	descripcion = models.CharField(max_length=300)
	orden = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural="Bloques de preguntas"
		ordering = ['tipoacta','idbloque']

	def __str__(self):
		return "{} : {}".format(self.tipoacta.idtipoacta, self.descripcion)

class Pregunta(ClaseModelo2):
	bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)
	idpregunta = models.CharField(max_length=10)
	descripcion = models.TextField()
	orden = models.FloatField(default=0)
	habilitada=models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Variables a Evaluar'
		ordering = ['orden']


	def __str__(self):
		return "{}".format(self.descripcion)


class EvaluacionPregunta(ClaseModelo2):
	evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	puntaje = models.FloatField()


class Establecimiento(ClaseModelo2):
	nitcc = models.CharField(max_length=30, unique=True)
	razonsocial = models.CharField(max_length=150)
	nroinscripcion = models.CharField(max_length=30)
	nombrecomercial = models.CharField(max_length=150)
	direccion = models.CharField(max_length=150)
	telefono = models.CharField(max_length=80)
	fax = models.CharField(max_length=20, null=True, blank=True)
	nromatricula = models.CharField(max_length=30)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='Dptoubica')
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpioubica')
	lugarubica = models.ForeignKey(LugarUbica, on_delete=models.CASCADE, null=True, blank=True)
	correoelectronico = models.EmailField(max_length=150, null=True, blank = True)
	propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, null=True, blank=True, \
	related_name='codpropietario')
	replegal = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='codreplegal')
	direccionotifica = models.CharField(max_length=150)
	dptonotifica= models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dptonotifica')
	mpionotifica= models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpionotifica')
	horariofunciona = models.CharField(max_length=150)
	nrotrabajadores = models.IntegerField()

	class Meta:
		verbose_name_plural="Establecimientos"

	def __str__(self):
		return "{}".format(self.razonsocial)


class ActaEstabEducativo(ClaseModelo2):
	fecha=models.DateField()
	nroacta=models.CharField(max_length=15)
	ciudad=models.CharField(max_length=30)
	establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
	nombrerector=models.CharField(max_length=100, null=True, blank=True)
	tipodocrector=models.ForeignKey(Tipodoc, on_delete=models.CASCADE, related_name='tipodocrector', null=True, blank=True)
	identificacionrector=models.CharField(max_length=20, null=True, blank=True)
	nroestjormanhombres=models.IntegerField(default=0)
	nroestjormanmujeres	=models.IntegerField(default=0)
	nroestjortarhombres=models.IntegerField(default=0)
	nroestjortarmujeres	=models.IntegerField(default=0)
	nroestjornochombres=models.IntegerField(default=0)
	nroestjornocmujeres	=models.IntegerField(default=0)
	nrodocenteshombres=models.IntegerField(default=1)
	nrodocentesmujeres=models.IntegerField(default=1)
	nroaulas=models.IntegerField(default=1)
	nropatios=models.IntegerField(default=0)
	nrocafeterias=models.IntegerField(default=0)
	fechaultinspeccion=models.DateField(null=True, blank=True)
	nroactaultinspeccion=models.CharField(max_length=15, null=True, blank=True)
	ultconcepto=models.ForeignKey(Concepto, on_delete=models.CASCADE, related_name='ultconcepto')
	motivoVisita=models.ForeignKey(MotivoVisita, on_delete=models.CASCADE, null=True, blank=True)
	concepto=models.ForeignKey(Concepto, on_delete=models.CASCADE, related_name='Concepto', null=True, blank=True)
	nrototalmuestrastomadas = models.IntegerField(null=True, blank=True, default=0)
	nroactatomamuestras = models.CharField(max_length=20, null=True, blank=True)
	requerimientosanitario=models.TextField(null=True, blank=True)
	observacionesanitarias=models.TextField(null=True, blank=True)
	observacionestablecimiento=models.TextField(null=True, blank=True)
	clausuratemptotal = models.BooleanField(default=False, verbose_name='Clausura temporal total')
	clausuratemparcial = models.BooleanField(default=False, verbose_name='Clausura temporal parcial')
	susparcialtrabajo = models.BooleanField(default=False, verbose_name='Suspensión parcial de trabajos o servicios')
	susptotaltrabservicio = models.BooleanField(default=False, verbose_name='Suspensión total de trabajos o servicios')
	aislamiento = models.BooleanField(default=False, verbose_name='Aislamiento o internación de personas para evitar la transmisión de enfermedades')
	decomiso = models.BooleanField(default=False, verbose_name='Decomiso')
	destruccion = models.BooleanField(default=False, verbose_name='Destrucción o desnaturalización')
	congelacion = models.BooleanField(default=False, verbose_name='Congelación')
	capturanimales = models.BooleanField(default=False, verbose_name='Captura y observación de animales sospechosos de enfermedades transmisibles')
	vacunacion = models.BooleanField(default=False, verbose_name='Vacunación personas o animales')
	controlinsectos = models.BooleanField(default=False, verbose_name='Control de insectos u otra fauna nociva o transmisora de enfermedades')
	desocupacion = models.BooleanField(default=False, verbose_name='Desocupación o desalojamiento de establecimientos o vivienda')
	nroactamedidasanitaria = models.CharField(max_length=20, null=True, blank=True)
	diashabileplazo = models.IntegerField(default=0, null=True, blank=True)
	fechainiplazo=models.DateField(null=True, blank=True)
	fechafinplazo=models.DateField(null=True, blank=True)

	class Meta:
		verbose_name='Acta de visita a establecimiento educativo'


	def __str__(self):
		return "{} {}".format(self.nroacta, self.establecimiento) 

class ItemActaEstabEducativo(ClaseModelo2):
	actaestabeducativo = models.ForeignKey(ActaEstabEducativo, on_delete=models.CASCADE)
	pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	evaluacion=models.ForeignKey(Evaluacion, on_delete=models.CASCADE, default=3)
	hallazgos=models.TextField(null=True, blank=True)
	puntaje=models.FloatField(default=0)
	habilitada=models.BooleanField(default=True)

class ActaEstEduFuncionario(ClaseModelo2):
	actaestabeducativo = models.ForeignKey(ActaEstabEducativo, on_delete=models.CASCADE)
	funcionario = models.ForeignKey(Funcionario, on_delete = models.CASCADE)

	def __str__(self):
		return "{}".format(self.funcionario)

class Atiende_ActaEstabEduc(ClaseModelo2):
	actaestabeducativo = models.ForeignKey(ActaEstabEducativo, on_delete=models.CASCADE)
	tipodoc = models.ForeignKey(Tipodoc, on_delete=models.CASCADE)
	nombre=models.CharField(max_length=100)
	identificacion = models.CharField(max_length=20)
	institucion = models.CharField(max_length=100, null=True, blank=True)
	cargo=models.CharField(max_length=80, null=True, blank=True)










#Expendio de carnes
#class ActaMsf012(ClaseModelo2): 



