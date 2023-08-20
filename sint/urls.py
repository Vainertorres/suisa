
from django.contrib import admin
from django.urls import path

from .views import  SintomaticoList, SintomaticoCreate, SintomaticoEdit, geolocDetallado, \
geolocMapaCalor, GrafSintomas, Principal

app_name='sint'

urlpatterns = [
    path('easytb', Principal.as_view(), name='easytb'),
    path('sintomatico/', SintomaticoList.as_view(), name='sintomatico_list'),
    path('sintomatico/new', SintomaticoCreate.as_view(), name='sintomatico_new'),
    path('sintomatico/edit/<int:pk>', SintomaticoEdit.as_view(), name='sintomatico_edit'),
    path('sintomatico/est/sintomas', GrafSintomas.as_view(), name='estadistica_sintomas'),    
    path('geolocdet', geolocDetallado, name='geoloc_detallado'),
    path('geolocmapcalor', geolocMapaCalor, name='geoloc_mapa_calor'),




]