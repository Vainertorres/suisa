from django.contrib import admin

# Register your models here.

from .models import OtraInstObjetoQueja, Serviciosobjqueja, TipoRespuestaPqrs

admin.site.register(OtraInstObjetoQueja)
admin.site.register(Serviciosobjqueja)
admin.site.register(TipoRespuestaPqrs)



