from django.urls import path
from .views import importCie10, DiagnosticoList, importRips, Grafdiagnosticoscie10, Home, \
DiagnosticoUpdate, DiagnosticoCreate, Archivocontrolist, Archivoconsultalist, ListadoDiagnostico, \
georrefenciarDiagCE, geolocMapaCalorDiagCE, mapaCalarDiagCE, listarRipsCargados

app_name='bai'


urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('importcie10', importCie10, name='Import_cie10'),
	path('rips', importRips, name='importar_rips'),
	path('cie10/estcoom', Grafdiagnosticoscie10.as_view(), name='estadistica_cie10'),
	path('cie10', DiagnosticoList.as_view(), name='cie10list'),
	path('cie10/edit/<int:pk>', DiagnosticoUpdate.as_view(), name='cie10_edit'),
	path('cie10/new', DiagnosticoCreate.as_view(), name='cie10_new'),
	path('rips/ctrl', Archivocontrolist.as_view(), name='rips_control'),
	path('rips/listar/<int:id>', listarRipsCargados, name='rips_listar'),
	path('rips/ce', Archivoconsultalist.as_view(), name='rips_consulta'),
	path('rips/grce', ListadoDiagnostico.as_view(), name='georref_ce'),
	path('rips/grce/<int:iddiag>', georrefenciarDiagCE, name='georref_ce_map'),
	path('rips/grmcce/<int:iddiag>', geolocMapaCalorDiagCE, name='georref_mapcalor_ce'),
	path('rips/mapacalorce/<int:iddiag>', mapaCalarDiagCE, name='mapcalor_ce'),





]