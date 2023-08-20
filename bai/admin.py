from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.

from .models import Finalidad, CausaExterna, Diagnosticos, ImportarCie10, AmbitoProcedimiento, Cups,\
Cums, FinalidadProcedimiento, DestinoSalida, EstadoSalida, FormaRealizactoQx, PersonalAsistencial, \
TipoMedicamento, TipoServicio, ViaIngreso, PeriodoImportRips, Tipousuario



class DiagnosticosResource(resources.ModelResource):
	class Meta:
		model = Diagnosticos

class DiagnosticosAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields = ['descripcion']
	list_display  = ('codigo','descripcion',)
	resource_class= DiagnosticosResource

admin.site.register(Finalidad)
admin.site.register(CausaExterna)
admin.site.register(Diagnosticos, DiagnosticosAdmin)
admin.site.register(ImportarCie10)
admin.site.register(AmbitoProcedimiento)
admin.site.register(Cups)
admin.site.register(Cums)
admin.site.register(FinalidadProcedimiento)
admin.site.register(DestinoSalida)
admin.site.register(EstadoSalida)
admin.site.register(FormaRealizactoQx)
admin.site.register(PersonalAsistencial)
admin.site.register(TipoMedicamento)
admin.site.register(TipoServicio)
admin.site.register(ViaIngreso)
admin.site.register(PeriodoImportRips)
admin.site.register(Tipousuario)



























