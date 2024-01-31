from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

from cnf.models import Eps, ClaseModelo2, Tipodoc, Sexo, Departamento, Municipio, Area, Etnia, \
ActividadEconomica, Ips, Regimen, Paciente, Pais


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

class GrupoSisbenIV(ClaseModelo2):
	codigo=models.CharField(max_length=1, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name="Grupo categoria sisben IV"
		verbose_name_plural="Grupos categorias sisben IV"
		ordering=['descripcion']


	def __str__(self):
		return "{}".format(self.descripcion)


class SubgrupoSisbenIV(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=150)
	gruposisbeniv=models.ForeignKey(GrupoSisbenIV, on_delete=models.CASCADE)

	class Meta:
		verbose_name="Sub grupo categoria sisben IV"
		verbose_name_plural="Sub grupos categorias sisben IV"
		ordering=['descripcion']


	def __str__(self):
		return "{} : {}".format(self.codigo, self.descripcion)


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
    tblpais = Pais.objects.filter(codigo='57').first()

    reg = Regimen.objects.filter(codigo='S').first()

    objpac = Paciente.objects.filter(tipodoc_id=td, identificacion=ident).first()
    if objpac:
    	objpac.eps = instance.eps
    	objpac.regimen = reg
    	objpac.fechanac = instance.fechanac
    	if tblpais:
    		objpac.pais = tblpais
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
    	objpac.eps = instance.eps
    	if tblpais:
    		objpac.pais = tblpais

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

@receiver(post_save, sender=Maestrocont)
def user_cont_sub_guardar(sender,instance,**kwargs):
    td = instance.tipodoc.id
    ident = instance.identificacion
    tbletnia = Etnia.objects.filter(id=6).first()
    tblpais = Pais.objects.filter(codigo='57').first() #Pais colombia

    reg = Regimen.objects.filter(codigo='C').first()

    objpac = Paciente.objects.filter(tipodoc_id=td, identificacion=ident).first()
    if objpac:
    	objpac.eps = instance.eps
    	objpac.regimen = reg
    	objpac.fechanac = instance.fechanac
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
    	objpac.etnia = tbletnia
    	objpac.departamento = instance.departamento
    	objpac.municipio = instance.municipio
    	objpac.eps = instance.eps
    	objpac.direccion = ''
    	if reg:
    		objpac.regimen = reg
    	if tblpais:
    		objpac.pais = tblpais
    objpac.save()


class OpcDesaprueba(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name='Opción de desaprobación'
		verbose_name_plural='Opciones de desaprobación'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class Formularioafil(ClaseModelo2):
	ESTADOAPRUEBA=(('A','Aprobar'),
		('D','Desaprobar'),
		('X','Sin Evaluar'))	
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	fechafiliacion = models.DateField()
	tipoafiliado = models.ForeignKey(Tipoafiliado, on_delete=models.CASCADE, null=True, blank=True)
	aprobar = models.CharField(max_length=1, choices=ESTADOAPRUEBA, default='X')    
	opcdesaprueba=models.ForeignKey(OpcDesaprueba, on_delete=models.CASCADE, null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)
	
	class Meta:
		verbose_name='Formularios de Afiliación'
		ordering=['-fechafiliacion']

class NovedadBdua(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion=models.CharField(max_length=255)

	class Meta:
		verbose_name="Configurar novedad"
		verbose_name_plural="Configurar novedades"
		ordering=['descripcion']

	def __str__(self):
		return "{} : {}".format(self.codigo, self.descripcion)

class CausalRetiro(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=255)

	class Meta:
		verbose_name = 'Causal de retiro'
		verbose_name_plural = 'Causales de retiros'
		ordering=['descripcion']


	def __str__(self):
		return "{} : {}".format(self.codigo, self.descripcion)


class RepNovedad(ClaseModelo2):
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)
	novedadbdua = models.ForeignKey(NovedadBdua, on_delete=models.CASCADE)
	fecha=models.DateField()
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	fecininovedad=models.DateField()
	valor1=models.CharField(max_length=20, null=True, blank=True)
	valor2=models.CharField(max_length=20, null=True, blank=True)
	valor3=models.CharField(max_length=20, null=True, blank=True)
	valor4=models.CharField(max_length=20, null=True, blank=True)
	valor5=models.CharField(max_length=20, null=True, blank=True)
	valor6=models.CharField(max_length=20, null=True, blank=True)
	valor7=models.CharField(max_length=20, null=True, blank=True)

	class Meta:
		verbose_name='Reporte de novedad'
		verbose_name_plural='Reportes de novedades'

	def __str__(self):
		return "{}".format(self.descripcion)

class TipoReporteSat(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=255)

	class Meta:
		verbose_name = 'Tipo de reporte SAT'
		verbose_name_plural = 'Tipos de reportes SAT'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class Sat(ClaseModelo2):
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, related_name='eps_origen')
	epsdest = models.ForeignKey(Eps, on_delete=models.CASCADE, related_name='eps_destino', null=True, blank=True)
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	tiporeportesat=models.ForeignKey(TipoReporteSat, on_delete=models.CASCADE)
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	fechanovedad=models.DateField(null=True, blank=True)
	nronovedad=models.CharField(max_length=80, null=True, blank=True)
	nivelsisben=models.ForeignKey(Nivelsisben, on_delete=models.CASCADE, null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Sistema de Afiliación Transaccional'
		verbose_name='Sistemas de Afiliacines Transaccionales'

	def __str__(self):
		return "{} : {}".format(self.fechanovedad, self.paciente)



class TiPobElegibleSub(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=255)

	class Meta:
		verbose_name = 'Tipo de población elegible para el régimen subsidiado'
		verbose_name_plural = 'Tipos de población elegible para el régimen subsidiado'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)


class ListadoCensal(ClaseModelo2):
	fechareg=models.DateField()
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='Paciente')	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	resguardo = models.ForeignKey(Resguardo, on_delete=models.CASCADE, null=True, blank=True)
	tipobelegiblebub = models.ForeignKey(TiPobElegibleSub, on_delete=models.CASCADE, null=True, blank=True)
	titular = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='titular', null=True, blank=True)	

	class Meta:
		verbose_name='Listado censal'
		verbose_name='Listados censales'

	def __str__(self):
		return "{} : {}".format(self.fechareg, self.paciente)

class ContribSolidaria(ClaseModelo2):
	ESTADO=(('AC','Activo'),
		('RE','Retirado'))
	fechaingreso=models.DateField()	
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, related_name='eps')
	regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE, related_name='regimen')
	categoria=models.CharField(max_length=80, null=True, blank=True)
	fechaliquidacion=models.DateField()	
	estado = models.CharField(max_length=2, choices=ESTADO, default='AC')    
	valor=models.FloatField(default=0,null=True, blank=True)
	atendido=models.BooleanField(default=False, null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Contribución solidaria'

	def __str__(self):
		return "{} : {}".format(self.fechaingreso, self.paciente)


class PoblacionsinSisben(ClaseModelo2):
	SISBENIZADO=(('SI','SI'),
		('NO','NO'),
		('NS','NO SABE'))	
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	categoria=models.CharField(max_length=80, null=True, blank=True)
	sisbenizado = models.CharField(max_length=2, choices=SISBENIZADO, default='NO')    
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Población sin encuesta sisbén'

	def __str__(self):
		return "{}".format(self.paciente)

class Modalidad(ClaseModelo2):
	codigo=models.CharField(max_length=2, unique=True)
	descripcion = models.CharField(max_length=255)

	class Meta:
		verbose_name = 'Modalidad de aseguramiento'
		verbose_name_plural = 'Modalidades de aseguramientos'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)


class PoblacionEspsinLS(ClaseModelo2):
	SISBENIZADO=(('SI','SI'),
		('NO','NO'),
		('NS','NO SABE'))	
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	modalidad=models.ForeignKey(Modalidad, on_delete=models.CASCADE, null=True, blank=True)	
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Población especial sin listado censal'

	def __str__(self):
		return "{}".format(self.paciente)

class SIAseguramiento(ClaseModelo2):
	cuentaconsi = models.BooleanField(default=True)
	realizacruces=models.BooleanField(default=True)
	bdcruces=models.CharField(max_length=80, null=True, blank=True)
	herramientasw=models.CharField(max_length=80, null=True, blank=True)
	responsable=models.CharField(max_length=150, null=True, blank=True)
	cargo=models.CharField(max_length=80, null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Sistema de información utilizado'

	def __str__(self):
		return "{}".format(self.herramientasw)

class PlanCobertura(ClaseModelo2):
	titulo = models.CharField(max_length=255)
	descactividad=models.TextField(null=True, blank=True)
	fechainicio = models.DateField()
	fechafin = models.DateField()
	responsable=models.CharField(max_length=255, null=True, blank=True)
	timpodedicado = models.IntegerField(default=1)
	indicador = models.CharField(max_length=255, null=True, blank=True)
	meta=models.TextField(null=True, blank=True)
	resultado=models.TextField(null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)

	
	class Meta:
		verbose_name='Plan de cobertura'

	def __str__(self):
		return "{}".format(self.titulo)


class AfilOficioSinSisben(ClaseModelo2):
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	modalidad=models.ForeignKey(Modalidad, on_delete=models.CASCADE, null=True, blank=True)	
	usuarioencuestado=models.BooleanField(default=False)
	fechaencuesta=models.DateField(null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Afiliado de oficio sin encuesta sisben IV'

	def __str__(self):
		return "{}".format(self.paciente)


class AfilSubGrupo5SinSisben(ClaseModelo2):
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	modalidad=models.ForeignKey(Modalidad, on_delete=models.CASCADE, null=True, blank=True)	
	usuarioencuestado=models.BooleanField(default=False)
	fechaencuesta=models.DateField(null=True, blank=True)
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Afiliado subsidiado grupo 5 sin encuesta sisben IV'

	def __str__(self):
		return "{}".format(self.paciente)

class Movilidad(ClaseModelo2):
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dpto_movilidad')	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpio_movilidad')
	departamentosis=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dpto_movilidad_sisben')	
	municipiosis=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpio_movilidad_sisben')
	nivelsisbenpe=models.CharField(max_length=80, null=True, blank=True)
	nrofuasat=models.CharField(max_length=80, null=True, blank=True)
	usuarioregsat=models.BooleanField(default=False)
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE)
	regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
	subgruposisbeniv=models.ForeignKey(SubgrupoSisbenIV, on_delete=models.CASCADE, null=True, blank=True)
	tipoafiliado = models.ForeignKey(Tipoafiliado, on_delete=models.CASCADE, null=True, blank=True)
	fechasolicitud=models.DateField()
	fechaefectivamov=models.DateField(null=True, blank=True)	
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Movilidad'

	def __str__(self):
		return "{}".format(self.paciente)

class SegPortabilidad(ClaseModelo2):
	ESTADO=(('AC','Activo'),
		('RE','Retirado'),
		('SU','Suspendido'))
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dpto_portabilidad')	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpio_portabilidad')
	departamentodest=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dpto_portabilidad_destino')	
	municipiodest=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpio_portabilidad_destino')
	fechasolicitud=models.DateField()
	fechaaplicacion=models.DateField(null=True, blank=True)	
	fechaatencion=models.DateField(null=True, blank=True)	
	estado = models.CharField(max_length=2, choices=ESTADO, default='AC')    
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Seguimiento Portabilidad'

	def __str__(self):
		return "{}".format(self.paciente)

class Portabilidades(ClaseModelo2):
	ESTADO=(('AC','Activo'),
		('RE','Retirado'),
		('SU','Suspendido'))
	paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)	
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dpto_porta')	
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpio_porta')
	departamentodest=models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='dpto_porta_destino')	
	municipiodest=models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='mpio_porta_destino')
	fechasolicitud=models.DateField()
	fechaatencion=models.DateField(null=True, blank=True)	
	fechaasignaips=models.DateField(null=True, blank=True)	
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE, null=True, blank=True)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	estado = models.CharField(max_length=2, choices=ESTADO, default='AC')    
	observacion=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name='Portabilidad'

	def __str__(self):
		return "{}".format(self.paciente)

class NovLcRegTipo1(ClaseModelo2):
	TIPOENTIDAD=(('MU','Municipio'),
		('DE','Departamento'),
		('DI','Distrito'))
	tiporegistro=models.IntegerField(default=1)
	tipoentidad=models.CharField(max_length=2,choices=TIPOENTIDAD, default='MU')
	nroidententidad=models.CharField(max_length=20)
	fechafinal=models.DateField()
	nrototalreg=models.IntegerField(default=0)

	class Meta:
		verbose_name='Novedad listados censal registro tipo 1'

	def __str__(self):
		return "{} : {}".format(self.tipoentidad, self.nroidententidad)

class CausActDocumento(ClaseModelo2):
	codigo=models.CharField(max_length=1)
	descripcion=models.CharField(max_length=80)

	class Meta:
		verbose_name = 'Causa de actualización de documentos'
		verbose_name_plural = 'Causales de actualización de documentos'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class NovLcRegTipo2(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=2)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc2')
	identificacion=models.CharField(max_length=16)
	tipodocnew=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc2new')
	identificacionnew=models.CharField(max_length=16)
	causactdocumento = models.ForeignKey(CausActDocumento, on_delete=models.CASCADE)
	fechaaplicanovedad=models.DateField()

	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 2'

	def __str__(self):	
		return "{} : {} : {}".format(self.tipodoc, self.identificacion,self.causactdocumento)

class NovLcRegTipo3(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=3)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc3')
	identificacion=models.CharField(max_length=16)
	nombre1new=models.CharField(max_length=60)
	nombre2new=models.CharField(max_length=60, null=True, blank=True)	

	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 3'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)

class NovLcRegTipo4(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=4)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc4')
	identificacion=models.CharField(max_length=16)
	apellido1new=models.CharField(max_length=60)
	apellido2new=models.CharField(max_length=60, null=True, blank=True)	

	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 4 Apellidos'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)

#Actualización del municipio
class NovLcRegTipo5(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=5)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc5')
	identificacion=models.CharField(max_length=16)
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 5 Municipio'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)

class EstadoLC(ClaseModelo2):
	codigo=models.CharField(max_length=1, unique=True)
	descripcion=models.CharField(max_length=150)

	class Meta:
		verbose_name='Estado del integrante de listado censal'

	def __str__(self):
		return "{}".format(self.descripcion)


#Actualización del estado
class NovLcRegTipo6(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=6)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE)
	identificacion=models.CharField(max_length=16)	
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	estadolc=models.ForeignKey(EstadoLC, on_delete=models.CASCADE)

	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 6 Cambio de estado'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)

#Actualización del Sexo
class NovLcRegTipo7(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=7)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE)
	identificacion=models.CharField(max_length=16)	
	sexo=models.ForeignKey(Sexo, on_delete=models.CASCADE, null=True, blank=True)
	

	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 7 Sexo'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)
	

#Actualización de fecha de nacimiento
class NovLcRegTipo8(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=8)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE)
	identificacion=models.CharField(max_length=16)	
	fechanac=models.DateField()
	

	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 8 Sexo'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)
	

#Actualización de CONDICION ELEGIBLE
class NovLcRegTipo9(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=9)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE)
	identificacion=models.CharField(max_length=16)	
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE)
	tipobelegiblesub=models.ForeignKey(TiPobElegibleSub, on_delete=models.CASCADE)

	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 9 Condición elegible'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)
	
#Actualización de Poblacion Especial
class NovLcRegTipo10(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=10)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE)
	identificacion=models.CharField(max_length=16)	
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, related_name='novlc10_pobesp')
	tipopoblacionespnew=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, related_name='novlc10_pobesp_new')
	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 10 Población especial'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)
	

#Actualización de identificación del titular
class NovLcRegTipo11(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=11)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc11')
	identificacion=models.CharField(max_length=16)	
	tipodoctitular=models.ForeignKey(Tipodoc,on_delete=models.CASCADE, related_name='tdnovlc11titular')
	identificaciontitular=models.CharField(max_length=16)	
		
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 11 identificación del titular'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)
	

#Eliminación
class NovLcRegTipo12(ClaseModelo2):
	novlcregtipo1=models.ForeignKey(NovLcRegTipo1, on_delete=models.CASCADE)
	tiporegistro=models.IntegerField(default=12)
	tipodoc=models.ForeignKey(Tipodoc,on_delete=models.CASCADE)
	identificacion=models.CharField(max_length=16)	
	tipopoblacionesp=models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE)
	
	class Meta:
		verbose_name='Detalle novedad listado censal registro tipo 12 Eliminación'

	def __str__(self):	
		return "{} : {}".format(self.tipodoc, self.identificacion)

class TipoTraslado(ClaseModelo2):
	codigo=models.CharField(max_length=1, unique=True)
	descripcion=models.CharField(max_length=150)

	class Meta:
		verbose_name = 'Tipo de traslado'
		verbose_name_plural = 'Tipos de traslados'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)


class NovedadS1(ClaseModelo2):
	TIPONOV=(('VAL','VALIDADAS'),
		('NEG','NEGADAS'))
	epssol=models.ForeignKey(Eps, on_delete=models.CASCADE, related_name='novs1epsol')
	tipodoc=models.ForeignKey(Tipodoc, on_delete=models.CASCADE, related_name='tpdocbduas1')
	identificacion = models.CharField(max_length=20)
	apellido1=models.CharField(max_length=60)
	apellido2=models.CharField(max_length=60, null=True, blank=True)
	nombre1=models.CharField(max_length=60)
	nombre2=models.CharField(max_length=60, null=True, blank=True)
	fechanac=models.DateField()
	sexo=models.ForeignKey(Sexo, on_delete=models.CASCADE, related_name='novs1sex')
	tipodocact=models.ForeignKey(Tipodoc, on_delete=models.CASCADE, related_name='tpdocacts1')
	identificacionact = models.CharField(max_length=20)
	apellido1act=models.CharField(max_length=60)
	apellido2act=models.CharField(max_length=60, null=True, blank=True)
	nombre1act=models.CharField(max_length=60)
	nombre2act=models.CharField(max_length=60, null=True, blank=True)
	fechanacact=models.DateField()
	sexoact=models.ForeignKey(Sexo, on_delete=models.CASCADE, related_name='novs1sexact')
	departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
	municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)
	area=models.ForeignKey(Area, on_delete=models.CASCADE)
	fechafilnov=models.DateField()
	tipopoblacionesp = models.ForeignKey(Tipopoblacionesp, on_delete=models.CASCADE, null=True, blank=True)
	nivelsisben=models.ForeignKey(Nivelsisben, on_delete=models.CASCADE, null=True, blank=True)
	tipotraslado=models.ForeignKey(TipoTraslado, on_delete=models.CASCADE, null=True, blank=True)
	metodologiagp=models.ForeignKey(Metodologiagp, on_delete=models.CASCADE, null=True, blank=True)
	subgruposisbeniv=models.ForeignKey(SubgrupoSisbenIV, on_delete=models.CASCADE, null=True, blank=True)
	condiscapacidad=models.CharField(max_length=1, null=True, blank=True)
	tipodocabfam=models.ForeignKey(Tipodoc, on_delete=models.CASCADE, null=True, blank=True, related_name='tipodocabfams1')
	identificacioncabfam=models.CharField(max_length=20, null=True, blank=True)
	parentezcocf=models.ForeignKey(Parentezcocf, on_delete=models.CASCADE, null=True, blank=True)
	tipoafiliado=models.ForeignKey(Tipoafiliado, on_delete=models.CASCADE, null=True, blank=True)
	etnia=models.ForeignKey(Etnia, on_delete=models.CASCADE, null=True, blank=True)
	resguardo=models.ForeignKey(Resguardo, on_delete=models.CASCADE, null=True, blank=True)
	tiponovedad=models.CharField(max_length=3, choices=TIPONOV, default='NEG', null=True, blank=True)
	condiciondiscapacidad=models.ForeignKey(Condiciondiscapacidad, on_delete=models.CASCADE, null=True, blank=True)
	epsrecibe=models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True, related_name="epsrecibe")
	descglosa=models.TextField(null=True, blank=True)
	acciones=models.TextField(null=True, blank=True)

	class Meta:
		verbose_name="Novedad S1"

	def __str__(self):
		return "{}:{}".format(self.tipodoc, self.descripcion)



    
    
   
    





	










