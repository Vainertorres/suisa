from django.contrib import admin

from .models import Bac, ImportSivCvdFile, FileFichaIec, AmbitoAtencion, EstadoAfectacion, \
ClaseContacto
# Register your models here.

admin.site.register(Bac)
admin.site.register(ImportSivCvdFile)
admin.site.register(FileFichaIec)
admin.site.register(AmbitoAtencion)
admin.site.register(EstadoAfectacion)
admin.site.register(ClaseContacto)








