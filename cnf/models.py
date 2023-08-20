from django.db import models
from django.forms.models import model_to_dict
from django_userforeignkey.models.fields import UserForeignKey
from django.contrib.auth.models import User

from mpl_toolkits.basemap.test import Basemap
from geopy.geocoders import Nominatim
import time
import math


# Create your models here.


class ClaseModelo(models.Model):
    estado = models.BooleanField(default = True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE)
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True

class ClaseModelo2(models.Model):
    estado = models.BooleanField(default = True)
    fc = models.DateTimeField(auto_now_add=True)
    fm = models.DateTimeField(auto_now=True)
    uc = UserForeignKey(auto_user_add=True, verbose_name="Usuario automatio", related_name="+")
    um = UserForeignKey(auto_user=True, verbose_name="Usuario Modifica", related_name="+")

    class Meta:
        abstract = True

class ActividadEconomica(ClaseModelo2):
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=300)

    class Meta:
        verbose_name='Actividad Economica'
        ordering = ['descripcion']

    def __str__(self):
        return "{}".format(self.descripcion)

class Agente(ClaseModelo):
    codigo = models.CharField(max_length=3, unique=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Agentes" 

class Area(ClaseModelo):
    codigo = models.CharField(max_length=1, unique=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Areas"

class Tipodoc(ClaseModelo):
    codigo = models.CharField(max_length=3, unique=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}-{}".format(self.codigo, self.descripcion)

    class Meta:
        verbose_name_plural = "Tipo documentos"
        ordering=['descripcion']

class Pais(ClaseModelo):
    codigo = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Paises" 

class Departamento(ClaseModelo):
    codigo = models.CharField(max_length=2)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Departamentos" 
        ordering=['descripcion']

class Municipio(ClaseModelo):
    codigo = models.CharField(max_length=3)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Municipios" 
        ordering=['descripcion']

class Varbarrio(ClaseModelo2):
    codigo=models.CharField(max_length=3, unique=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Config Características de barrio"
        ordering = ['descripcion']


class Comuna(ClaseModelo):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Comunas"
        ordering=['descripcion']

class Barrio(ClaseModelo):
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=80)
    lat = models.CharField(max_length=20, blank = True, null=True, default='SD')
    lon = models.CharField(max_length=20, blank = True, null=True, default='SD')


    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Barrios"
        ordering=['descripcion']

class Caractbarrio(ClaseModelo2):
    TIPOCARACTBARRIO = (
        ('Debilidad', 'Debilidad'),
        ('Fortaleza', 'Fortaleza'),
        ('Otros', 'Otros'),
    )
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)
    varbarrio = models.ForeignKey(Varbarrio, on_delete=models.CASCADE)
    tipocaracteristica = models.CharField(max_length=10, choices=TIPOCARACTBARRIO)
    observacion=models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.tipocaracteristica)


class Institucion(ClaseModelo2):
    nit             = models.CharField(max_length=20)
    razonsocial     = models.CharField(max_length=150)
    encabezado      = models.TextField(null=True, blank=True)
    piedepagina     = models.TextField(null=True, blank=True)
    logo            = models.ImageField(upload_to='cnf')
    nomalcalde      = models.CharField(max_length=100, null = True, blank=True)
    nomsecsalud     = models.CharField(max_length=100, null = True, blank=True)
    correoelectronico = models.CharField(max_length=100, null=True, blank=True)
    departamento    = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    municipio       = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    barrio          = models.ForeignKey(Barrio, on_delete=models.CASCADE, null = True, blank= True) 
    direccion       = models.CharField(max_length=150, null = True, blank=True)
    telefono        = models.CharField(max_length=80, null = True, blank = True)

    class Meta:
        verbose_name='Institución'

    def __str__(self):
        return "{}".format(self.razonsocial)

class TomadorDecision(ClaseModelo2):
    institucion     = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    tipodoc         = models.ForeignKey(Tipodoc, on_delete=models.CASCADE)
    identificacion  = models.CharField(max_length=20)
    nombres         = models.CharField(max_length=80)
    apellidos       = models.CharField(max_length=80)
    direccion       = models.CharField(max_length=100, null=True, blank= True)
    telefono        = models.CharField(max_length=30, null=True, blank = True)
    correoelectronico = models.CharField(max_length=100, null=True, blank = True)    

    class Meta:
        verbose_name='Tomadores de Decisión'

    def __str__(self):
        return "{} {}".format(self.nombres, self.apellidos)

class ClasifCaso(ClaseModelo):
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Clasifiación de casos"
        ordering=['descripcion']


class ClasiFinal(ClaseModelo):
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Clasificación Final"
        ordering=['descripcion']

class ClasiFinicial(ClaseModelo):
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Clasificación Inicial"
        ordering=['descripcion']


class CondiccionFinal(ClaseModelo):
    codigo = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Condicción Final"
        ordering=['descripcion']

class Coomorbilidad(ClaseModelo):
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Coomorbilidades"
        ordering=['descripcion']

class Regimen(ClaseModelo):
    codigo = models.CharField(max_length=1, unique=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Regimenes"
        ordering=['descripcion'] 

class Eps(ClaseModelo):
    regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=150)
    nomcontacto = models.CharField(max_length=150, blank=True, null=True)
    telcontacto = models.CharField(max_length=30, blank=True, null= True)
    direccion = models.CharField(max_length=100, blank= True, null= True)
    correoelectronico = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.descripcion, self.codigo)

    class Meta:
        verbose_name_plural = "Eps"
        ordering=['descripcion'] 

class Etnia(ClaseModelo):
    codigo = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Etnias"
        ordering=['descripcion']

class Evento(ClaseModelo):
    codigo = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return "{}:{}".format(self.codigo, self.descripcion)

    class Meta:
        verbose_name_plural = "Eventos"
        ordering=['descripcion']

class Fuente(ClaseModelo):
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Fuentes"
        ordering=['descripcion']

class Funcionario(ClaseModelo2):
    identificacion = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    correoelectronico = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        verbose_name='Funcionarios'

    def __str__(self):
        return "{} {}".format(self.nombres, self.apellidos)

class GrupoPob(ClaseModelo):
    descripcion= models.CharField(max_length=80, unique=True)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Grupos Poblacionales" #para referencia en Django en Plural
        ordering=['descripcion']

class Ips(ClaseModelo2):
    nit = models.CharField(max_length=15, unique=True)
    razonsocial = models.CharField(max_length=150)
    nomreplegal = models.CharField(max_length=80, null=True, blank=True)
    telcontacto = models.CharField(max_length=30, null=True, blank=True)
    codhabilitacion = models.CharField(max_length=20, null=True, blank=True)
    fechahabilitacion = models.DateField(null=True, blank=True)
    fechafinhabil=models.DateField(null=True, blank=True)


    def __str__(self):
        return "{}".format(self.razonsocial)

    class Meta:
        verbose_name_plural = "IPS" #para referencia en Django en Plural
        ordering=['razonsocial']

class Muestra(ClaseModelo):
    codigo = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Muestras"
        ordering=['descripcion']

class Ocupacion(ClaseModelo):
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Ocupaciones" #Ocupaciones
        ordering=['descripcion']

class Parentezco(ClaseModelo2):
    descripcion = models.CharField(max_length=80)

    class Meta:
        verbose_name='Parentezco'
        ordering=['descripcion']

    def __str__(self):
        return "{}".format(self.descripcion)

class Prueba(ClaseModelo):
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural='Pruebas'
        ordering=['descripcion']

    def __str__(self):
        return "{}".format(self.descripcion)


class Resultado(ClaseModelo):
    codigo = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Resultados"
        ordering=['descripcion']

class SemEpidemiologica(ClaseModelo):
    codigo = models.IntegerField(unique=True)
    anio = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=80)

    class Meta:
        ordering=['-codigo']
        verbose_name_plural = "Semanas Epidemiologicas"

    def __str__(self):
        return "{}".format(self.descripcion)
        ordering=['descripcion']

class Sexo(ClaseModelo):
    codigo = models.CharField(max_length=1, unique=True)
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Sexos"
        ordering=['descripcion']

class Sintoma(ClaseModelo):
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Sintomas"
        ordering=['descripcion']


class Tipocontacto(ClaseModelo2):
    descripcion=models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)
    class Meta:
        verbose_name_plural = "Tipo de contacto"
        ordering=['descripcion'] 

class Tipoconglomerado(ClaseModelo2):
    descripcion=models.CharField(max_length=80)

    def __str__(self):
        return "{}".format(self.descripcion)
    class Meta:
        verbose_name_plural = "Categoría de Conglomerados"
        ordering=['descripcion'] 

class TipoTrabajo(ClaseModelo2):
    descripcion = models.CharField(max_length=100)

    class Meta:
        verbose_name='Tipo de Trabajo Realizado'
        ordering = ['descripcion']

    def __str__(self):
        return "{}".format(descripcion)

class UmEdad(ClaseModelo):
    codigo = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.descripcion)

    class Meta:
        verbose_name_plural = "Unidades de medida"
        ordering=['descripcion'] 


class Upgd(ClaseModelo):
    nitcc = models.CharField(max_length=20, unique=True)
    razonsocial = models.CharField(max_length=150)
    nomcontacto = models.CharField(max_length=150, null=True, blank=True)
    telcontacto = models.CharField(max_length=30, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    correoelectronico = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.razonsocial)

    class Meta:
        verbose_name_plural = "UPGD"
        ordering=['razonsocial']

class Paciente(ClaseModelo2):
    tipodoc = models.ForeignKey(Tipodoc, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=20)    
    nombre1 = models.CharField(max_length=60)
    nombre2 = models.CharField(max_length=60, blank=True, null=True)
    apellido1 = models.CharField(max_length=60)
    apellido2 = models.CharField(max_length=60, blank=True, null=True)
    fechaNac = models.DateField(null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE,null=True, blank=True)
    direccion = models.CharField(max_length=150, blank= True, null= True)
    telefono = models.CharField(max_length=30, blank= True, null=True)
    correoelectronico = models.EmailField(max_length = 254, null=True, blank=True)     
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE, null=True, blank=True)
    eps = models.ForeignKey(Eps, on_delete=models.CASCADE, blank=True, null=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, blank=True, null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.CASCADE, null=True, blank=True)
    lat = models.CharField(max_length=20, blank = True, null=True, default='SD')
    lon = models.CharField(max_length=20, blank=True, null=True, default='SD')
    razonsocial = models.CharField(max_length=250)

    def toJson(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return '{}:{}'.format(self.identificacion, self.razonsocial)

    class Meta():
        unique_together= (('tipodoc', 'identificacion'),)
        verbose_name_plural="Pacientes"
        ordering = ['nombre1','nombre2', 'apellido1', 'apellido2']

    def save(self):
        nombre = self.nombre1

        if not (self.nombre2 == "" or self.nombre2==None or self.nombre2=='Nan'):
            nombre += " " + self.nombre2

        nombre += " " + self.apellido1
        if not (self.apellido2 == "" or self.apellido2==None or self.apellido2 =='Nan'):
            nombre += " " + self.apellido2
        self.razonsocial = nombre
        super(Paciente, self).save() #llamar al metodo guardar del padre


class RedLaboratorios(ClaseModelo2):
    descripcion = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    nomreplegal = models.CharField(max_length=100, null=True, blank=True)
    lat = models.CharField(max_length=20, blank = True, null=True, default='SD')
    lon = models.CharField(max_length=20, blank=True, null=True, default='SD')

    class Meta:
        verbose_name='Red de RedLaboratorios'
        ordering=['descripcion']

    def __str__(self):
        return "{}".format(self.descripcion)



            





     
    

