from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from cnf.models import ClaseModelo2, Ips, Paciente, UmEdad, Eps, Tipodoc, Regimen, Sexo, Departamento, \
Municipio, Area

# Create your models here.

class AmbitoProcedimiento(ClaseModelo2):
	codigo=models.IntegerField(unique=True)
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Ambito de procedimientos'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class Cups(ClaseModelo2):
	codigo = models.CharField(max_length=10, unique=True)
	descripcion = models.CharField(max_length=300)

	class Meta:
		verbose_name = 'Código Cups'
		verbose_name_plural = 'Códigos Cups'
		ordering = ['descripcion']

	def __str__(self):
		return "{}:{}".format(self.codigo, self.descripcion)

class Cums(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
	ESTADO = (
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    )
	expediente = models.IntegerField(null=True, blank=True)
	producto = models.CharField(max_length=200, null=True, blank=True)
	titular = models.CharField(max_length=200, null=True, blank=True)
	regsanitario = models.CharField(max_length=150, null=True, blank=True)
	fechaexpedicion = models.DateField(null=True, blank =True)
	fechavencimiento = models.DateField(null=True, blank =True)
	estadoregistro = models.CharField(max_length=100, null=True, blank =True)
	expedientecum = models.CharField(max_length=20, null=True, blank =True)
	consecutivocum = models.IntegerField(null=True, blank=True)
	cantidadcum = models.CharField(max_length=20, blank=True, null=True)
	descripcioncomercial = models.CharField(max_length=300)
	estado = models.CharField(max_length=10, choices=ESTADO, null=True, blank=True, default='Activo')
	fechaactivo = models.DateField(null=True, blank=True)
	fechainactivo = models.DateField(null=True, blank=True)
	muestramedica = models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	unidad = models.CharField(max_length=10, null=True, blank=True)
	atc = models.CharField(max_length=20, null=True, blank=True)
	descripcionatc = models.CharField(max_length=300, null=True, blank=True)
	viaadministracion = models.CharField(max_length=80, null=True, blank=True)
	concentracion = models.CharField(max_length=10, null=True, blank=True)
	principioactivo = models.CharField(max_length=300, null=True, blank=True)
	unidadmedida = models.CharField(max_length=50, null=True, blank=True)
	cantidad = models.CharField(max_length=20,null=True, blank=True)
	unidadreferencia = models.CharField(max_length=100,null=True, blank=True)
	formafarmaceutica = models.CharField(max_length=100,null=True, blank=True)
	nombrerol = models.CharField(max_length=100,null=True, blank=True)
	tiporol = models.CharField(max_length=50, null=True, blank=True)
	modalidad = models.CharField(max_length=50, null=True, blank=True)


	class Meta:
		verbose_name = 'Medicamento'
		verbose_name_plural = 'Listado de Medicamentos'
		ordering = ['descripcioncomercial']

	def __str__(self):
		return "{}:{}".format(self.codigo, self.descripcioncomercial)

class FinalidadProcedimiento(ClaseModelo2):
	codigo = models.IntegerField()
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name='Finalidad del procedimientos'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class ImportarCie10(ClaseModelo2):
	file_name = models.FileField(upload_to='bai', null=True, blank=True)
	file_cups=models.FileField(upload_to='bai',null=True, blank=True)
	file_cums=models.FileField(upload_to='bai',null=True, blank=True)
	uploaded =models.DateField(auto_now_add=True)
	activated= models.BooleanField(default=False)

	def __str__(self):
		return f"Id del Archivo {self.id}"

class Finalidad(ClaseModelo2):
	codigo = models.CharField(max_length=2)
	descripcion = models.CharField(max_length=80)

	def __str__(self):
		return "{}".format(self.descripcion)

	class Meta:
		verbose_name_plural="Finalidad de consulta"
		ordering=['descripcion']

class CausaExterna(ClaseModelo2):
	codigo = models.CharField(max_length=2)
	descripcion = models.CharField(max_length=80)

	def __str__(self):
		return "{}".format(self.descripcion)

	class Meta:
		verbose_name_plural="Causa Externa"
		ordering=['descripcion']	

class Diagnosticos(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
	codigo=models.CharField(max_length=16)
	descripcion = models.CharField(max_length=300)
	notifobligatoria = models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	idcapitulo = models.IntegerField()
	capitulo = models.CharField(max_length=300)
	codcie3=models.CharField(max_length=3)
	descripcie3= models.CharField(max_length=300)

	def __str__(self):
		return "{} - {}".format(self.codigo, self.descripcion)

	class Meta:
		verbose_name_plural="Diagnosticos"
		ordering=['descripcion']	


class DestinoSalida(ClaseModelo2):
	codigo=models.IntegerField(unique=True)	
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name='Desntino a la salida'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class EstadoSalida(ClaseModelo2):
	codigo=models.IntegerField(unique=True)	
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Estado a la salida'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class FormaRealizactoQx(ClaseModelo2):
	codigo=models.IntegerField(unique=True)
	descripcion = models.CharField(max_length=100)

	class Meta:
		verbose_name='Forma de realización acto Quirurgico'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class PersonalAsistencial(ClaseModelo2):
	codigo=models.IntegerField(unique=True)	
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name='Personal Asistencial'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class PeriodoImportRips(ClaseModelo2):
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	fecharemision= models.DateField()
	fileCT = models.FileField(upload_to='bai')
	fileAF = models.FileField(upload_to='bai')
	fileAU = models.FileField(upload_to='bai', null=True, blank=True)
	fileUS = models.FileField(upload_to='bai')
	fileAH = models.FileField(upload_to='bai', null=True, blank=True)
	fileAT = models.FileField(upload_to='bai', null=True, blank=True)
	fileAC = models.FileField(upload_to='bai', null=True, blank=True)
	fileAP = models.FileField(upload_to='bai', null=True, blank=True)
	fileAM = models.FileField(upload_to='bai', null=True, blank=True)
	fileAN = models.FileField(upload_to='bai', null=True, blank=True)
	activated = models.BooleanField(default=False)

	class Meta:
		verbose_name='Periodo a Importar Rips'
		ordering = ['-fecharemision']

	def __str__(self):
		return "{} - {}".format(self.ips, self.fecharemision)



class TipoMedicamento(ClaseModelo2):
	codigo=models.IntegerField(unique=True)	
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Tipo de Medicamento'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class TipoServicio(ClaseModelo2):
	codigo = models.CharField(max_length=1, unique=True)
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Tipo de Servicio'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class TipoDiagPrincipal(ClaseModelo2):
	codigo = models.IntegerField()
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Tipo de Diagnóstico Principal'
		ordering=['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)


class ViaIngreso(ClaseModelo2):
	codigo=models.IntegerField(unique=True)
	descripcion = models.CharField(max_length=50)

	class Meta:
		verbose_name='Vía de Ingreso a la Institución'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class RipsControl(ClaseModelo2):
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	fecharemision = models.DateField()
	codarchivo = models.CharField(max_length=10)
	totalreg = models.IntegerField()
	periodoimportRips = models.ForeignKey(PeriodoImportRips, on_delete= models.CASCADE, null=True, blank=True)

	def __str__(self):
		return "{} - {}".format(self.ips, self.fecharemision)

	class Meta:
		verbose_name_plural = 'Rips de control'

class Tipousuario(ClaseModelo2):
	codigo=models.IntegerField()
	descripcion=models.CharField(max_length=100)
	regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		verbose_name="Tipo de usuario"
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)

class RipsUsuarios(ClaseModelo2):
	tipodoc = models.ForeignKey(Tipodoc, on_delete=models.CASCADE)
	identificacion = models.CharField(max_length=20)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	tipousuario = models.ForeignKey(Tipousuario, on_delete=models.CASCADE, null=True, blank=True)
	apellido1 = models.CharField(max_length=60)
	apellido2 = models.CharField(max_length=60, null=True, blank=True)
	nombre1 = models.CharField(max_length=60)
	nombre2 = models.CharField(max_length=60, null=True, blank=True)
	edad = models.IntegerField(default=0, null=True, blank=True)
	umedad = models.ForeignKey(UmEdad, on_delete=models.CASCADE, null=True, blank=True)
	sexo = models.ForeignKey(Sexo,on_delete=models.CASCADE, null=True, blank=True)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null= True, blank = True)
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null= True, blank = True)
	area = models.ForeignKey(Area, on_delete=models.CASCADE, null= True, blank = True)
	razonsocial = models.CharField(max_length=250, null=True, blank=True)

	class Meta:
		verbose_name='Rips de Usuarios'
		ordering = ['razonsocial']

	def __str__(self):
		strdato = self.nombre1
		if len(self.nombre2) > 0:
			strdato += ' ' + self.nombre2

		strdato += ' ' + self.apellido1
		if len(self.apellido2) > 0:
			strdato += ' ' + self.apellido2

		return "{}".format(strdato)

	def save(self):
		nombre = self.nombre1
		if self.nombre2==0:
			self.nombre2=''

		if self.apellido2==0:
			self.apellido2=''

		if not (self.nombre2 == ""):
			nombre += " " + self.nombre2

		nombre += " " + self.apellido1

		if not (self.apellido2 == ""):
			nombre += " " + self.apellido2

		self.razonsocial = nombre
		super(RipsUsuarios, self).save() #llamar al metodo guardar del padre

@receiver(post_save, sender=RipsUsuarios)
def ripsuser_guardar_paciente(sender,instance,**kwargs):
    td = instance.tipodoc.id
    ident = instance.identificacion
    regtipousuario = instance.tipousuario.regimen_id
    reg = Regimen.objects.filter(pk=regtipousuario).first()

    objpac = Paciente.objects.filter(tipodoc_id=td, identificacion=ident).first()
    if objpac:
    	pass
    else:
    	objpac = Paciente()
    	objpac.tipodoc = instance.tipodoc
    	objpac.identificacion = instance.identificacion
    	objpac.apellido1 = instance.apellido1
    	objpac.apellido2 = instance.apellido2
    	objpac.nombre1 = instance.nombre1
    	objpac.nombre2 = instance.nombre2
    	#objpac.fechanac = instance.fechanac
    	objpac.sexo = instance.sexo
    	objpac.departamento = instance.departamento
    	objpac.municipio = instance.municipio
    	objpac.direccion = ''

    	if reg:
    		objpac.regimen = reg
    objpac.save()

class RipsTransaccion(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	fechaexpfac = models.DateField()
	fechainicio = models.DateField(null=True, blank=True)
	fechafinal = models.DateField(null=True, blank=True)
	eps = models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	nrocontrato  = models.CharField(max_length=15, null=True, blank=True)
	planbeneficio = models.CharField(max_length=30, null=True, blank=True)
	nropoliza = models.CharField(max_length=10, null=True, blank=True)
	vlrtotalcopago = models.FloatField(null=True, blank=True, default=0)
	vlrcomision = models.FloatField(null=True, blank=True, default=0)
	vlrdescuento = models.FloatField(null=True, blank=True, default=0)
	vlrnetopagar= models.FloatField(null=True, blank=True, default=0)
	periodoimportrips = models.ForeignKey(PeriodoImportRips, on_delete= models.CASCADE, null=True, blank=True)
	
	class Meta:
		verbose_name='Rips de Transacciones'

	def __str__(self):
		return "Ips: {} : Factura No. {}".format(self.ips, self.nrofactura)

class RipsConsulta(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
	fechacons = models.DateField(null=True, blank=True)
	nroautoriza = models.CharField(max_length=15, null=True, blank=True)
	cups = models.ForeignKey(Cups, on_delete=models.CASCADE, null=True, blank=True)
	finalidad = models.ForeignKey(Finalidad, on_delete=models.CASCADE)
	causaExterna = models.ForeignKey(CausaExterna, on_delete=models.CASCADE)
	vlrconsulta = models.FloatField(default=0)
	vlrcuotamodera = models.FloatField(default=0)
	vlrneto = models.FloatField(default=0)
	edad = models.IntegerField(null=True, blank=True)
	umEdad = models.ForeignKey(UmEdad, on_delete=models.CASCADE)
	periodoimportrips = models.ForeignKey(PeriodoImportRips, on_delete= models.CASCADE, null=True, blank=True)


	def __str__(self):
		return "{}-{}".format(self.fechacons, self.paciente)

	class Meta:
		verbose_name_plural = "Rips de consulta"
		ordering=['fechacons','paciente']

class DiagRipsCons(ClaseModelo2):
	SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )
	ripsconsulta = models.ForeignKey(RipsConsulta, on_delete=models.CASCADE)
	diagnostico = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE)
	diagppal =  models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	tipodiagprincipal = models.ForeignKey(TipoDiagPrincipal,on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return "{} Dx Principal: {}".format(self.diagnostico, self.diagppal)

	class Meta:
		verbose_name_plural = "Diagnostico Rips Consulta"
		ordering=['diagppal','diagnostico']

class RipsProcedimiento(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
	fechaprocedimiento = models.DateField(null=True, blank=True)
	nroautoriza = models.CharField(max_length=15, null=True, blank=True)
	cups = models.ForeignKey(Cups, on_delete=models.CASCADE)
	ambitoprocedimiento = models.ForeignKey(AmbitoProcedimiento, on_delete=models.CASCADE, null=True, blank=True)
	finalidad = models.ForeignKey(FinalidadProcedimiento, on_delete=models.CASCADE, null=True, blank=True)
	personalasistencial = models.ForeignKey(PersonalAsistencial, on_delete=models.CASCADE, null=True, blank= True)
	formarealizactoqx = models.ForeignKey(FormaRealizactoQx, on_delete=models.CASCADE, null=True, blank=True)
	valorprocedimiento = models.FloatField(default=0)

	def __str__(self):
		return "{}-{}".format(self.fechaprocedimiento, self.paciente)

	class Meta:
		verbose_name_plural = "Rips de procedimientos"
		ordering=['fechaprocedimiento','paciente']

class DiagProcedimiento(ClaseModelo2):
	SINOCOMP = (
        ('DP', 'Diagnostico principal'),
        ('DR', 'Diagnóstivo relacionado'),
        ('DC', 'Complicación'),
    )
	ripsprocedimiento = models.ForeignKey(RipsProcedimiento, on_delete=models.CASCADE)
	diagnostico = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE)
	diagppal =  models.CharField(max_length=2, choices=SINOCOMP, null=True, blank=True, default='DR')
	
	def __str__(self):
		return "{} Dx Principal: {}".format(self.diagnostico, self.diagppal)

	class Meta:
		verbose_name_plural = "Diagnostico"
		ordering=['diagppal','diagnostico']


class RipsUrgencia(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
	fechaingreso=models.DateField()
	horaingreo = models.TimeField(auto_now=False, auto_now_add=False)
	nroautoriza = models.CharField(max_length=15, null=True, blank=True)
	causaexterna = models.ForeignKey(CausaExterna, on_delete=models.CASCADE)
	destinosalida = models.ForeignKey(DestinoSalida, on_delete=models.CASCADE)
	estadosalida = models.ForeignKey(EstadoSalida, on_delete=models.CASCADE)
	diagmuerte = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE, null=True, blank=True)
	fechasalida = models.DateField()
	horasalida = models.TimeField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return "{}-{}".format(self.fechaingreso, self.paciente)

	class Meta:
		verbose_name_plural = "Rips de Urgencia"
		ordering=['fechaingreso','paciente']


class DiagRipsUrgencia(ClaseModelo2):
	SINO = (
        ('SI', 'Diagnóstico principal'),
        ('NO', 'Diagnostico relacionado'),
    )
	ripsurgencia = models.ForeignKey(RipsUrgencia, on_delete=models.CASCADE)
	diagnostico = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE)
	diagppal =  models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')

	def __str__(self):
		return "{} Dx Principal: {}".format(self.diagnostico, self.diagppal)

	class Meta:
		verbose_name_plural = "Diagnostico Rips Consulta"
		ordering=['diagppal','diagnostico']



class RipsHospitalizacion(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
	viaingreso = models.ForeignKey(ViaIngreso, on_delete=models.CASCADE)
	fechaingreso=models.DateField()
	horaingreo = models.TimeField(auto_now=False, auto_now_add=False)
	nroautoriza = models.CharField(max_length=15, null=True, blank=True)
	causaexterna = models.ForeignKey(CausaExterna, on_delete=models.CASCADE)
	diagppalingreso = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE, null=True, blank=True, related_name='dxingreso')
	diagcomplicaciones = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE, null=True, blank=True, related_name='dxcomplicacion')
	estadosalida = models.ForeignKey(EstadoSalida, on_delete=models.CASCADE, null=True, blank=True)
	diagmuerte = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE, null=True, blank=True, related_name='dxmuerte')
	fechasalida = models.DateField()
	horasalida = models.TimeField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return "{}-{}".format(self.fechaingreso, self.paciente)

	class Meta:
		verbose_name_plural = "Rips de Urgencia"
		ordering=['fechaingreso','paciente']



class DiagRipsHospitaliza(ClaseModelo2):
	SINO = (
        ('SI', 'Diagnóstico principal'),
        ('NO', 'Diagnostico relacionado'),
    )
	ripshospitalizacion = models.ForeignKey(RipsHospitalizacion, on_delete=models.CASCADE)
	diagnostico = models.ForeignKey(Diagnosticos, on_delete=models.CASCADE)
	diagppal =  models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')

	def __str__(self):
		return "{} Dx Principal: {}".format(self.diagnostico, self.diagppal)

	class Meta:
		verbose_name_plural = "Diagnostico Egreso hospitalizacion"
		ordering=['diagppal','diagnostico']



class RipsMedicamento(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
	nroautoriza = models.CharField(max_length=15, null=True, blank=True)
	cums = models.ForeignKey(Cums, on_delete=models.CASCADE)
	tipomedicamento = models.ForeignKey(TipoMedicamento, on_delete=models.CASCADE)
	nombregenerico = models.CharField(max_length=300)
	formafarmaceutica = models.CharField(max_length=100)
	concentracion = models.CharField(max_length=80)
	unidadmedida = models.CharField(max_length=50)
	numerodeunidades = models.FloatField(default=1)
	valorunitario = models.FloatField(default=0)
	valortotal = models.FloatField(default=0)

	def __str__(self):
		return "{}-{}".format(self.nrofactura, self.paciente)

	class Meta:
		verbose_name_plural = "Rips de Medicamentos"
		ordering=['nrofactura','paciente']

class RipsOtrosServicios(ClaseModelo2):
	ripscontrol = models.ForeignKey(RipsControl, on_delete=models.CASCADE)
	nrofactura = models.CharField(max_length=20)
	ips = models.ForeignKey(Ips, on_delete=models.CASCADE)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
	nroautoriza = models.CharField(max_length=15, null=True, blank=True)
	tiposervicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
	codigoservicio = models.CharField(max_length=15, null=True, blank=True)
	nombreservicio = models.CharField(max_length=300)
	cantidad = models.FloatField(default=0)
	valorunitario = models.FloatField(default=0)
	valortotal = models.FloatField(default=0)
	
	def __str__(self):
		return "{}-{}".format(self.nrofactura, self.paciente)

	class Meta:
		verbose_name_plural = "Rips otros servicios"
		ordering=['nrofactura','paciente']

	

