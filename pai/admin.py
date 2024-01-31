from django.contrib import admin

from .models import VacunaCovid, RediarioCargado, Biologico, Dosisbiologico, Jeringas, \
RediarioPaiRegCargado

# Register your models here.
admin.site.register(VacunaCovid)
admin.site.register(RediarioCargado)
admin.site.register(Biologico)
admin.site.register(Dosisbiologico)
admin.site.register(Jeringas)
admin.site.register(RediarioPaiRegCargado)



