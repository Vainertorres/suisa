from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import PropietarioList, PropietarioEdit, PropietarioCreate, EstablecimientoList, \
EstablecimientoCreate, EstablecimientoEdit, homesam, EstablecimientoEducativoList, \
establecimientoEducativoCreate

app_name='sam'

urlpatterns = [

path('propietario', PropietarioList.as_view(), name='propietario_list'),
path('propietario/new', PropietarioCreate.as_view(), name='propietario_new'),
path('propietario/edit/<int:pk>', PropietarioEdit.as_view(), name='propietario_edit'),
path('establecimiento', EstablecimientoList.as_view(), name='establecimiento_list'),
path('establecimiento/new', EstablecimientoCreate.as_view(), name='establecimiento_new'),
path('establecimiento/edit/<int:pk>', EstablecimientoEdit.as_view(), name='establecimiento_edit'),
path('home', homesam, name='home'),
path('actaestedu/list/<int:pk>', EstablecimientoEducativoList.as_view(), name='actaestedu_list'),
path('actaestedu/new/<int:estaedu_id>', establecimientoEducativoCreate, name='actaestedu_new'),
path('actaestedu/update/<int:estaedu_id>/<int:idacta>', establecimientoEducativoCreate, name='actaestedu_update'),



]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)