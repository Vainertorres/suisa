from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

from cnf.models import Eps, ClaseModelo2, Tipodoc, Sexo, Departamento, Municipio, Area, Etnia, \
ActividadEconomica, Ips, Regimen, Paciente


class Tipopoblacionesp(ClaseModelo2):
	codigo = models.CharField(max_length=2, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name='Tipo de población especial'

	def __str__(self):
		return "{}".format(self.descripcion)


class Metodologiagp(ClaseModelo2):
	codigo = models.CharField(max_length=1, unique=True)
	descripcion = models.CharField(max_length=80)
	
	class Meta:
		verbose_name = 'Metodología Grupo Poblacional'

	def __str__(self):
		return "{}".format(self.descripcion)

class Parentezcocf(ClaseModelo2):
	codigo = models.CharField(max_length=1, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name="Parentesco con el cabeza de familia"

	def __str__(self):
		return "{}".format(self.descripcion)


class Resguardo(ClaseModelo2):
	codigo = models.CharField(max_length=3, unique = True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name="Resguardos indígenas"

	def __str__(self):
		return "{}".format(self.descripcion)

class MaestrobduaCargado(ClaseModelo2):
	fecha = models.DateField()
	file_name = models.FileField(upload_to='aseguramiento')
	uploaded =models.DateField(auto_now_add=True)
	activated= models.BooleanField(default=False)


	def save(self):
		#self.uc = instance.request.user
		super(MaestrobduaCargado, self).save()

	def __str__(self):
		return f"Id del Archivo {self.id}"

class Nivelsisben(ClaseModelo2):
	codigo  = models.CharField(max_length=1, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name="Nivel del sisben"

	def __str__(self):
		return "{}".format(self.descripcion)

class Condiciondiscapacidad(ClaseModelo2):
	codigo  = models.CharField(max_length=2, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name="Condición de discapacidad"

	def __str__(self):
		return "{}".format(self.descripcion)


class Maestrosub(ClaseModelo2):
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	tipodoc = models.ForeignKey(Tipodoc, on_delete=models.CASCADE, related_name='tipodocuser')
	identificacion = models.CharField(max_length=20)
	apellido1 = models.CharField(max_length=60)
	apellido2 = models.CharField(max_length=60, null = True, blank=True)
	nombre1 = models.CharField(max_length=60)
	nombre2 = models.CharField(max_length=60, null=True, blank=True)
	fechanac = models.DateField()
	sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	fechaafiliacion = models.DateField()
	tipopoblacionesp =models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	nivelsisben = models.ForeignKey(Nivelsisben, on_delete=models.CASCADE, null=True, blank=True)
	codigoipsprimaria = models.CharField(max_length=12)
	metodologiagp = models.ForeignKey(Metodologiagp, on_delete=models.CASCADE, null=True, blank=True)
	subgruposisbeniv = models.CharField(max_length=3, null=True, blank=True)
	condiciondiscapacidad = models.ForeignKey(Condiciondiscapacidad, on_delete=models.CASCADE, null=True, blank=True)
	tipodoccabezafam = models.ForeignKey(Tipodoc, on_delete=models.CASCADE, null=True, blank=True, \
					related_name = 'tipodoccabfam')
	identificacioncabfam = models.CharField(max_length=20, null=True, blank=True)
	parentezcocf = models.ForeignKey(Parentezcocf, on_delete=models.CASCADE, null=True, blank=True)
	tipoafiliado = models.CharField(max_length=1)
	etnia = models.ForeignKey(Etnia, on_delete=models.CASCADE, null=True, blank=True)
	resguardo = models.ForeignKey(Resguardo, on_delete=models.CASCADE, null=True, blank=True)
	ipsodontologica = models.CharField(max_length=12, null=True, blank=True)
	estadoafil = models.CharField(max_length=3) 
	razonsocial = models.CharField(max_length=250)

	class Meta():
		verbose_name="Maestro subsidiado"

	def save(self):
		razsoc = self.nombre1

		nomb2 = self.nombre2

		if isinstance(nomb2, str):
			nomb2 = self.nombre2.strip()

		if nomb2 != "" or nomb2 != "0" or nomb2 != 0:
			pass
		else: 
			razsoc = razsoc + " " + nomb2

		razsoc += ' ' + self.apellido1

		apell2 = self.apellido2

		if isinstance(apell2, str):
			apell2 = self.apellido2.strip()

		if apell2 != "" or apell2 != "0" or apell2 != 0:
			pass
		else: 
			razsoc = razsoc + " " + apell2
		
		self.razonsocial = razsoc
		super(Maestrosub, self).save() #llamar al metodo guardar del padre

	def __str__(self):
		return "{}-{} {}".format(self.tipodoc, self.identificacion, self.razonsocial)



@receiver(post_save, sender=Maestrosub)
def user_sub_guardar(sender,instance,**kwargs):
    td = instance.tipodoc.id
    ident = instance.identificacion

    reg = Regimen.objects.filter(codigo='S').first()

    objpac = Paciente.objects.filter(tipodoc_id=td, identificacion=ident).first()
    if objpac:
    	objpac.eps = instance.eps
    else:
    	objpac = Paciente()
    	objpac.tipodoc = instance.tipodoc
    	objpac.identificacion = instance.identificacion
    	objpac.apellido1 = instance.apellido1
    	objpac.apellido2 = instance.apellido2
    	objpac.nombre1 = instance.nombre1
    	objpac.nombre2 = instance.nombre2
    	objpac.fechanac = instance.fechanac
    	objpac.sexo = instance.sexo
    	objpac.etnia = instance.etnia
    	objpac.departamento = instance.departamento
    	objpac.municipio = instance.municipio
    	objpac.direccion = ''

    	if reg:
    		objpac.regimen = reg
    objpac.save()

class Tipocontizante(ClaseModelo2):
	codigo=models.CharField(max_length=2, unique=True)
	descripcion = models.CharField(max_length=200)

	class Meta:
		verbose_name="Tipo de cotizante"

	def __str__(self):
		return "{}".format(self.descripcion)

class Tipoafiliado(ClaseModelo2):
	codigo=models.CharField(max_length=1, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name="Tipo de Afiliado"

	def __str__(self):
		return "{}".format(self.descripcion)

class Maestrocont(ClaseModelo2):
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	tipodoccotizante = models.ForeignKey(Tipodoc, on_delete=models.CASCADE, null=True, blank=True, \
	related_name="Tipodoc_cotiza")
	identcotizante=models.CharField(max_length=20, null=True, blank=True)
	tipodoc=models.ForeignKey(Tipodoc, on_delete=models.CASCADE, related_name="Tipodocumento")
	identificacion=models.CharField(max_length=20)
	apellido1 = models.CharField(max_length=60)
	apellido2 = models.CharField(max_length=60, null=True, blank=True)
	nombre1=models.CharField(max_length=60)
	nombre2=models.CharField(max_length=60, null=True, blank=True)
	fechanac = models.DateField()
	sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE)
	tipocotizante=models.ForeignKey(Tipocontizante, on_delete=models.CASCADE, null=True, blank=True)
	tipoafiliado=models.ForeignKey(Tipoafiliado, on_delete=models.CASCADE, null=True, blank=True)
	condiciondiscapacidad = models.ForeignKey(Condiciondiscapacidad, on_delete=models.CASCADE, null=True, blank=True)
	parentezcocf = models.ForeignKey(Parentezcocf, on_delete=models.CASCADE, null=True, blank=True)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	fechaafiliacion = models.DateField()
	tipodocaportante = models.ForeignKey(Tipodoc, on_delete=models.CASCADE, null=True, blank=True, \
	related_name="Tipodoc_aporta")
	identaportante=models.CharField(max_length=20, null=True, blank=True)
	actividadeconomica = models.ForeignKey(ActividadEconomica, on_delete=models.CASCADE, null=True, blank=True)
	ipsprimaria = models.ForeignKey(Ips, on_delete=models.CASCADE, null=True, blank=True, related_name="Ipsprimaria")
	ipsodontologica = models.ForeignKey(Ips, on_delete=models.CASCADE, null=True, blank=True, related_name="Ipsodontologica")
	estadoactual = models.CharField(max_length=2, null=True, blank=True)
	razonsocial = models.CharField(max_length=250)


	class Meta:
		verbose_name="Maestro Contributivo"

	def toJSON(self):
		item = model_to_dict(self)
		return item


	def save(self):
		razsoc = self.nombre1

		nomb2 = self.nombre2

		if isinstance(nomb2, str):
			nomb2 = self.nombre2.strip()

		if nomb2 != "" or nomb2 != "0" or nomb2 != 0:
			pass
		else: 
			razsoc = razsoc + " " + nomb2


		razsoc += ' ' + self.apellido1

		apell2 = self.apellido2

		if isinstance(apell2, str):
			apell2 = self.apellido2.strip()


		if apell2 != "" or apell2 != "0" or apell2 != 0:
			pass
		else: 
			razsoc = razsoc + " " + apell2

		
		self.razonsocial = razsoc
		super(Maestrocont, self).save() #llamar al metodo guardar del padre

	def __str__(self):
		return "{}-{} {}".format(self.tipodoc, self.identificacion, self.razonsocial)







	


	










