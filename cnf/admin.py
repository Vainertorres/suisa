from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import GrupoPob, Ocupacion, Regimen, Eps, Resultado, Muestra, Prueba, Agente, \
Sintoma, Coomorbilidad, Tipodoc, Pais, Departamento, Municipio, Comuna, Barrio, ClasifCaso, \
Sexo, UmEdad, Evento, Area, Etnia, ClasiFinicial, Upgd, Fuente, CondiccionFinal, ClasiFinal, \
Paciente, SemEpidemiologica, Tipocontacto, Tipoconglomerado, Ips, Parentezco, Funcionario, \
RedLaboratorios, ActividadEconomica, TipoTrabajo, Institucion, TomadorDecision, Varbarrio

# Register your models here.

class ActividadEconomicaResource(resources.ModelResource):
	class Meta:
		model = ActividadEconomica

class ActividadEconomicaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['descripcion']
	list_display  = ('codigo','descripcion',)
	resource_class= ActividadEconomicaResource


admin.site.register(SemEpidemiologica)
admin.site.register(GrupoPob)
admin.site.register(Ocupacion)
admin.site.register(Regimen)
admin.site.register(Eps)
admin.site.register(Resultado)
admin.site.register(Muestra)
admin.site.register(Prueba)
admin.site.register(Agente)
admin.site.register(Sintoma)
admin.site.register(Coomorbilidad)
admin.site.register(Tipodoc)
admin.site.register(Pais)
admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Comuna)
admin.site.register(Barrio)
admin.site.register(ClasifCaso)
admin.site.register(Sexo)
admin.site.register(UmEdad)
admin.site.register(Evento)
admin.site.register(Area)
admin.site.register(Etnia)
admin.site.register(CondiccionFinal)
admin.site.register(ClasiFinal)
admin.site.register(Fuente)
admin.site.register(ClasiFinicial)
admin.site.register(Upgd)
admin.site.register(Paciente)
admin.site.register(Tipocontacto)
admin.site.register(Tipoconglomerado)
admin.site.register(Ips)
admin.site.register(Parentezco)
admin.site.register(Funcionario)
admin.site.register(RedLaboratorios)
admin.site.register(ActividadEconomica, ActividadEconomicaAdmin)
admin.site.register(TipoTrabajo)
admin.site.register(Institucion)
admin.site.register(TomadorDecision)
admin.site.register(Varbarrio)





















