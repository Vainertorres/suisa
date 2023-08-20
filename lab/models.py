from django.db import models

# Create your models here.

from cnf.models import ClaseModelo2, Paciente, Muestra, RedLaboratorios


class TipoExamen(ClaseModelo2):
	codigo = models.CharField(max_length=10, null=True, blank=True)
	descripcion = models.CharField(max_length=100)
	
	class Meta:
		verbose_name='Tipo de Laboratorio'

	def __str__(self):
		return "{}".format(self.descripcion)


class RepLaboratorio(ClaseModelo2):
	RESULTADO = (
        ('POS', 'Positivo'),
        ('NEG', 'Negativo'),
    )
	paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	fechamuestra = models.DateField()
	muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE)
	redlaboratorios = models.ForeignKey(RedLaboratorios, on_delete=models.CASCADE)
	tipoexamen  = models.ForeignKey(TipoExamen, on_delete=models.CASCADE) 
	resultado = models.CharField(max_length=3, choices=RESULTADO, null=True, blank=True)
	fecharesultado = models.DateField(null=True, blank=True)

	class Meta:
		verbose_name='Reporte de Laboratorios'
		ordering = ['fechamuestra']

	def __str__(self):
		return "Paciente: {}, Muestra: {}, Resultado: {}".format(self.paciente, self.muestra, self.resultado)




