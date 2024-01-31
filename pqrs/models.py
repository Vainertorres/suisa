from django.db import models
from cnf.models import ClaseModelo2, Paciente, Eps, Ips

# Create your models here.

class Serviciosobjqueja(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=150)

	class Meta:
		ordering=['descripcion']

	def __str__(self):
		return '{}'.format(self.descripcion)

class OtraInstObjetoQueja(ClaseModelo2):
	nitcc=models.CharField(max_length=30, unique=True)
	razonsocial=models.CharField(max_length=150)

	def __str__(self):
		return "{}".format(self.razonsocial)

class TipoRespuestaPqrs(ClaseModelo2):
	codigo=models.CharField(max_length=3, unique=True)
	descripcion = models.CharField(max_length=80)

	class Meta:
		verbose_name = 'Tipo de respuesta PQRS'
		verbose_name_plural = 'Tipo de respuesta PQRS'
		ordering = ['descripcion']

	def __str__(self):
		return "{}".format(self.descripcion)



class Pqrs(ClaseModelo2):
	INSTQUEJA = (
        ('E', 'Eps'),
        ('I', 'Ips'),
        ('O', 'Otros'))
	SINO=(
		('SI', 'SI'),
		('NO','NO')
		)
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	fecha=models.DateField()
	edad=models.IntegerField(default=0)
	victima=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	desplazado=models.CharField(max_length=2, choices=SINO, null=True, blank=True)
	pqrscontra=models.CharField(max_length=1, choices=INSTQUEJA, null=True, blank=True)
	resolinmediata=models.BooleanField(default=False)
	eps=models.ForeignKey(Eps, on_delete=models.CASCADE, null=True, blank=True)
	ips=models.ForeignKey(Ips, on_delete=models.CASCADE, null=True, blank=True)
	otrainstobjetoqueja = models.ForeignKey(OtraInstObjetoQueja, on_delete=models.CASCADE, null=True, blank=True)
	periodoresolucion=models.IntegerField(default=1)
	iniciaderepeticion=models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	iniciatutela=models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	explicacion=models.TextField(null=True, blank=True)
	terderepeticion=models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	tertutela=models.CharField(max_length=2, choices=SINO, null=True, blank=True, default='NO')
	serviciosobjqueja=models.ManyToManyField(Serviciosobjqueja)
	respondida = models.BooleanField(default=False, null=True, blank=True)
	tiporespuestapqrs=models.ForeignKey(TipoRespuestaPqrs, on_delete=models.CASCADE, null=True, blank=True)
	fecharespuesta=models.DateField(null=True, blank=True)


	class Meta:
		ordering=['-fecha']


	def __str__(self):
		return '{} - {}'.format(self.fecha, self.paciente)

class SeguimientoPQRS(ClaseModelo2):
	pqrs=models.ForeignKey(Pqrs, on_delete=models.CASCADE)
	fecha=models.DateField()
	observacion=models.TextField()

	class Meta:
		verbose_name='Seguimiento Pqrs'

	def __str__(self):
		return "{}:{}".format(self.fecha, self.observacion)





