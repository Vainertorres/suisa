from django.contrib import admin

from .models import Propietario, Concepto, MotivoVisita, Evaluacion, TipoActa, Bloque, \
	                Pregunta, LugarUbica
# Register your models here.
admin.site.register(Propietario)
admin.site.register(Concepto)
admin.site.register(MotivoVisita)
admin.site.register(Evaluacion)
admin.site.register(TipoActa)
admin.site.register(Bloque)
admin.site.register(Pregunta)
admin.site.register(LugarUbica)








