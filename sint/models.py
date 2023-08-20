from django.db import models
from cnf.models import Paciente, ClaseModelo, ClaseModelo2

# Create your models here.
#class Entidadext(ClaseModelo2):


class TipoSintomatico(ClaseModelo):
    codigo= models.CharField(max_length=20, unique=True)	
    descripcion= models.CharField(max_length=80)
   
    class Meta:
        ordering = ['descripcion']
    
    def __str__(self):
        return "{}".format(self.descripcion)

class Sintomatico(ClaseModelo):

    SINO = (
        ('SI', 'Si'),
        ('NO', 'No'),
    )

    fecha=models.DateField()
    paciente=models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fiebre=models.CharField(max_length=2, choices=SINO, default='NO')
    cefalea= models.CharField(max_length=2, choices=SINO, default='NO')
    doloretrocular= models.CharField(max_length=2, choices=SINO, default='NO')
    mialgias= models.CharField(max_length=2, choices=SINO, default='NO')
    artralgias= models.CharField(max_length=2, choices=SINO, default='NO')
    rash= models.CharField(max_length=2, choices=SINO, default='NO')
    zona_endemica_dengue= models.CharField(max_length=2, choices=SINO, default='NO')
    tos= models.CharField(max_length=2, choices=SINO, default='NO')
    perdida_peso= models.CharField(max_length=2, choices=SINO, default='NO')
    sudor_nocturna= models.CharField(max_length=2, choices=SINO, default='NO')
    observacion=models.TextField(blank=True, null=True)
    tiposintomatico = models.ForeignKey(TipoSintomatico, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering= ['-fecha']

    def __str__(self):
        return "{}".format(self.observacion)





    



    


