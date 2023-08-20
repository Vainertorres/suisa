from django.contrib import admin
from django.urls import path


from .views import importarDengue210, dengueList, dengueEdit, SegPacDengueCreate, SegPacDengueEdit, \
inactivar_ficha_dengue, dengueGraveList, dengueMortalidadList, GrafDenguemes, FileDengueUpdate, \
FileDengueCreate, IecDengueCreate, IecDengueUpdate, ContactoIecDengueCreate, ContactoIecDengueUpdate, \
geolocDengue210, GrafDengueSemEpi, EstDengueSemEpi, Home, geolocDengue220, mapaCalarDengueGrave

app_name='den'   

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('dengue210/', importarDengue210, name='importar_dengue_210'),
	# path('dengue/', DengueList.as_view(), name='dengue_list'),
	path('dengue/210/', dengueList, name='dengue_list'),
	path('dengue/220/', dengueGraveList, name='dengue_grave_list'),
	path('dengue/580/', dengueMortalidadList, name='dengue_mortalidad_list'),
	path('dengue/del/<int:id>', inactivar_ficha_dengue, name='dengue_inact'),	 
	path('dengue/edit/<int:iddengue>', dengueEdit, name='dengue_edit'),
	path('dengue/render/<int:iddengue>', SegPacDengueCreate.as_view(), name='render_segpac_dengue'),
	path('dengue/segedit/<int:pk>',SegPacDengueEdit.as_view(), name='segpac_dengue_edit'),
	path('dengue/filedengue/new/<int:iddengue>', FileDengueCreate.as_view(), name='filedengue_new'),
	path('dengue/filedengue/edit/<int:pk>', FileDengueUpdate.as_view(), name='filedengue_edit'),
	path('dengue/iec/new/<int:iddengue>', IecDengueCreate.as_view(), name='iecdengue_new'),
	path('dengue/iec/edit/<int:pk>', IecDengueUpdate.as_view(), name='iecdengue_edit'),
    path('dengue/iec/contact/new/<int:idiecdengue>', ContactoIecDengueCreate.as_view(), name='contactiecdengue_new'),
	path('dengue/iec/contact/edit/<int:pk>', ContactoIecDengueUpdate.as_view(), name='contactiecdengue_edit'),
	path('dengue/estmes', GrafDenguemes.as_view(), name='est_dengue_mes'),
	path('dengue/est/selanioepi', EstDengueSemEpi.as_view(), name='est_dengue_selanioepi'),	 
	path('dengue/est/semepiu', GrafDengueSemEpi.as_view(), name='est_dengue_semepi'),
	path('dengue/geoloc210', geolocDengue210, name='geoloc_evento_210'),
	path('dengue/geoloc220', geolocDengue220, name='geoloc_evento_220'),
	path('dengue/mapcal220', mapaCalarDengueGrave, name='mapa_calor_220'),

	

	 
	 #path('dengue/new/<int:iddengue>', SegPacDengueCreate.as_view(), name='segpac_dengue_new'),

] 