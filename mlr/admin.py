from django.contrib import admin

# Register your models here.

from .models import EspecieInf, Tratamiento, ImportarMalaria

admin.site.register(EspecieInf)
admin.site.register(Tratamiento)
admin.site.register(ImportarMalaria)
