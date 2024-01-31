from django.contrib import admin

# Register your models here.

from .models import MaestrobduaCargado, Resguardo, Parentezcocf, Metodologiagp, Tipopoblacionesp, \
Condiciondiscapacidad, Nivelsisben, Tipocontizante, Tipoafiliado, NovedadBdua, \
CausalRetiro, OpcDesaprueba, TipoReporteSat, TiPobElegibleSub, Modalidad, SubgrupoSisbenIV, \
GrupoSisbenIV, CausActDocumento, EstadoLC, TipoTraslado

admin.site.register(CausalRetiro)
admin.site.register(CausActDocumento)
admin.site.register(Condiciondiscapacidad)
admin.site.register(EstadoLC)
admin.site.register(MaestrobduaCargado)
admin.site.register(Metodologiagp)
admin.site.register(Modalidad)
admin.site.register(NovedadBdua)
admin.site.register(Nivelsisben)
admin.site.register(OpcDesaprueba)
admin.site.register(Parentezcocf)
admin.site.register(Resguardo)
admin.site.register(Tipoafiliado)
admin.site.register(TiPobElegibleSub)
admin.site.register(Tipopoblacionesp)
admin.site.register(Tipocontizante)
admin.site.register(TipoReporteSat)
admin.site.register(TipoTraslado)
admin.site.register(GrupoSisbenIV)
admin.site.register(SubgrupoSisbenIV)




