from django.contrib import admin

# Register your models here.

from .models import MaestrobduaCargado, Resguardo, Parentezcocf, Metodologiagp, Tipopoblacionesp, \
Condiciondiscapacidad, Nivelsisben, Tipocontizante, Tipoafiliado


admin.site.register(MaestrobduaCargado)
admin.site.register(Resguardo)
admin.site.register(Parentezcocf)
admin.site.register(Metodologiagp)
admin.site.register(Tipopoblacionesp)
admin.site.register(Condiciondiscapacidad)
admin.site.register(Nivelsisben)
admin.site.register(Tipocontizante)
admin.site.register(Tipoafiliado)








