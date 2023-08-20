from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import importarMalaria, MalariaList, malariaEdit, SegPacMalariaEdit, SegPacMalariaCreate, \
geolocMalaria, geolocMapaCalorMalaria, ConglomeradoMalariaList, ConglomeradoMalariaCreate,\
ConglomeradoMalariaEdit, ConglomeradoPacMalariaCreate, ConglomeradoPacMalariaUpdate, \
SegConglomeradoMalariaUpdate, SegConglomeradoMalariaCreate, FileConglomeradoUpdate, \
FileConglomeradoCreate, GrafComplicacionMlr, GrafMalariaSemEpi, GrafMalariaBarrio, GrafMalariaEPS

app_name='mlr'

urlpatterns = [
path('importar', importarMalaria, name='importar_malaria'),
path('malaria', MalariaList.as_view(), name='malaria_list'),
path('malaria/edit/<int:idmalaria>', malariaEdit, name='malaria_edit'),
path('malaria/seg/edit/<int:pk>', SegPacMalariaEdit.as_view(), name='segmalaria_edit'),
path('malaria/seg/new/<int:idmalaria>', SegPacMalariaCreate.as_view(), name='segmalaria_new'),
path('malaria/geoloc', geolocMalaria, name='geoloc_malaria'),
path('malaria/geomapcalor', geolocMapaCalorMalaria, name='geomapcalor_malaria'),
path('conglomerado', ConglomeradoMalariaList.as_view(), name='conglomeradomlr_list'),
path('conglomerado/edit/<int:pk>', ConglomeradoMalariaEdit.as_view(), name='conglomeradomlr_edit'),
path('conglomerado/new', ConglomeradoMalariaCreate.as_view(), name='conglomeradomlr_new'),
path('conglo/pac/new/<int:idconglomerado>', ConglomeradoPacMalariaCreate.as_view(), name='pacconglomlr_new'),
path('conglo/pac/edit/<int:pk>', ConglomeradoPacMalariaUpdate.as_view(), name='pacconglomlr_edit'),
path('mlr/seg/conglo/edit/<int:pk>', SegConglomeradoMalariaUpdate.as_view(), name='segconglomalaria_edit'),
path('mlr/seg/conglo/new/<int:idconglomerado>',SegConglomeradoMalariaCreate.as_view(), name='segconglomalaria_new'),
path('mlr/arch/conglo/edit/<int:pk>', FileConglomeradoUpdate.as_view(), name='fileconglomalaria_edit'),
path('mlr/arch/conglo/new/<int:idconglomerado>',FileConglomeradoCreate.as_view(), name='fileconglomalaria_new'),
path('Graf/complicaciones',GrafComplicacionMlr.as_view(), name='est_complicacion_malaria'),
path('Graf/mlr/semepi',GrafMalariaSemEpi.as_view(), name='est_malaria_semepi'),
path('Graf/mlr/barrio',GrafMalariaBarrio.as_view(), name='est_malaria_barrio'),
path('Graf/mlr/eps',GrafMalariaEPS.as_view(), name='est_malaria_eps'),






]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)