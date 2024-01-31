from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import MaestrobduaList, importarmaestrobdua, Principal, importarmaestrocontributivo, \
	MaestrocontList, MaestroListSS, aseg_reload, dt_serverside, ContributivoListSS, aseg_reload_contributivo, \
	dt_serverside_contributivo, EstadisticaMS, EstadisticaMC, RepNovedadList, \
	RepNovedadCreate, RepNovedadUpdate, ReportNovedades, report_novedad_csv_view, \
	FormularioafilList, FormularioafilCreate, FormularioafilUpdate, SatList, SatCreate, \
	SatUpdate, ListadoCensaList, ListadoCensalCreate, ListadoCensalUpdate, ContribSolidariaList,\
	ContribSolidariaCreate, ContribSolidariaUpdate, PobSinSisbenList, PobSinSisbenCreate, \
	PobSinSisbenUpdate, PoblacionEspsinLSList,PoblacionEspsinLSCreate, PoblacionEspsinLSUpdate, \
	SIAseguramientoList, SIAseguramientoCreate, SIAseguramientoUpdate, \
	PlanCoberturaList, PlanCoberturaCreate, PlanCoberturaUpdate, AfilOficioSinSisbenList, \
	AfilOficioSinSisbenCreate, AfilOficioSinSisbenUpdate, AfilSubGrupo5SinSisbenList, \
	AfilSubGrupo5SinSisbenCreate, AfilSubGrupo5SinSisbenUpdate, MovilidadList, MovilidadCreate, \
	MovilidadUpdate, SegPortabilidadList, SegPortabilidadCreate, SegPortabilidadUpdate, \
	PortabilidadList, PortabilidadCreate, PortabilidadUpdate, NovLcRegTipo1List, \
	NovLcRegTipo1Update, NovLcRegTipo1Create, delete_novlcregtipo2, delete_novlcregtipo3, \
	delete_novlcregtipo4, delete_novlcregtipo5, delete_novlcregtipo6, delete_novlcregtipo7, \
	delete_novlcregtipo8, delete_novlcregtipo9, delete_novlcregtipo10, delete_novlcregtipo11, \
	delete_novlcregtipo12, report_novedadlc_csv_view

app_name='aseg'

urlpatterns = [
path('bdua', Principal.as_view(), name='bdua'),
path('maestrobdua/import', importarmaestrobdua, name='importar_maestrobdua'),
path('maestrobdua/list/', MaestrobduaList.as_view(), name='maestrobdua_list'),
path('maestrobdua/listss/', MaestroListSS.as_view(), name='maestrobdua_listss'),
path('maestrobdua/listsub/', aseg_reload, name='listar_subsidiado'),
path('maestrobdua/listss_reload/', dt_serverside, name='listss_reload'),
path('ms/est/eps', EstadisticaMS.as_view(), name='est_eps_sub'),
path('maestrocont/import', importarmaestrocontributivo, name='importar_maestrocont'),
path('maestrocont/list/', ContributivoListSS.as_view(), name='maestrocont_list'),
#path('maestrocont/listcont/', aseg_reload_contributivo, name='listar_contributivo'),
path('maestrocont/listss_reload/', dt_serverside_contributivo, name='listcont_reload'),
path('mc/est/eps', EstadisticaMC.as_view(), name='est_eps_cont'),
path('Repnovedad', RepNovedadList.as_view(), name='reporte_novedad_list'),
path('Repnovedad/add', RepNovedadCreate.as_view(), name='rep_novedad_create'),
path('Repnovedad/edit/<int:pk>', RepNovedadUpdate.as_view(), name='rep_novedad_edit'),
path('Repnovedad/report', ReportNovedades.as_view(), name='novedad_report'),
path('Repnovedad/txt/<str:fec_ini>/<str:fec_fin>', report_novedad_csv_view, name='export_novedad'),
path('fua/list', FormularioafilList.as_view(), name='fua_list'),
path('fua/add', FormularioafilCreate.as_view(), name='fua_create'),
path('fua/edit/<int:pk>', FormularioafilUpdate.as_view(), name='fua_edit'),
path('sat/list', SatList.as_view(), name='sat_list'),
path('sat/add', SatCreate.as_view(), name='sat_create'),
path('sat/edit/<int:pk>', SatUpdate.as_view(), name='sat_edit'),
path('listcensal/list', ListadoCensaList.as_view(), name='list_censal_list'),
path('listcensal/add', ListadoCensalCreate.as_view(), name='list_censal_create'),
path('listcensal/edit/<int:pk>', ListadoCensalUpdate.as_view(), name='list_censal_edit'),
path('contrisolid/list', ContribSolidariaList.as_view(), name='contr_solidaria_list'),
path('contrisolid/add', ContribSolidariaCreate.as_view(), name='contr_solidaria_create'),
path('contrisolid/edit/<int:pk>', ContribSolidariaUpdate.as_view(), name='contr_solidaria_edit'),
path('pobsinsisben/list', PobSinSisbenList.as_view(), name='pob_sin_sisben_list'),
path('pobsinsisben/add', PobSinSisbenCreate.as_view(), name='pob_sin_sisben_create'),
path('pobsinsisben/edit/<int:pk>', PobSinSisbenUpdate.as_view(), name='pob_sin_sisben_edit'),
path('pobespsinlc/list', PoblacionEspsinLSList.as_view(), name='pobespsinlc_list'),
path('pobespsinlc/add', PoblacionEspsinLSCreate.as_view(), name='pobespsinlc_create'),
path('pobespsinlc/edit/<int:pk>', PoblacionEspsinLSUpdate.as_view(), name='pobespsinlc_edit'),
path('siutilizado/list', SIAseguramientoList.as_view(), name='siutilizado_list'),
path('siutilizado/add', SIAseguramientoCreate.as_view(), name='siutilizado_create'),
path('siutilizado/edit/<int:pk>', SIAseguramientoUpdate.as_view(), name='siutilizado_edit'),
path('plancob/list', PlanCoberturaList.as_view(), name='plan_cobertura_list'),
path('plancob/add', PlanCoberturaCreate.as_view(), name='plan_cobertura_create'),
path('plancob/edit/<int:pk>', PlanCoberturaUpdate.as_view(), name='plan_cobertura_edit'),
path('Afilofisinsisben/list', AfilOficioSinSisbenList.as_view(), name='Afil_ofi_sin_sisben_list'),
path('Afilofisinsisben/add', AfilOficioSinSisbenCreate.as_view(), name='Afil_ofi_sin_sisben_create'),
path('Afilofisinsisben/edit/<int:pk>', AfilOficioSinSisbenUpdate.as_view(), name='Afil_ofi_sin_sisben_edit'),
path('afilsubg5sinsisben/list', AfilSubGrupo5SinSisbenList.as_view(), name='afil_sub_g5_sin_sisben_list'),
path('afilsubg5sinsisben/add', AfilSubGrupo5SinSisbenCreate.as_view(), name='afil_sub_g5_sin_sisben_create'),
path('afilsubg5sinsisben/edit/<int:pk>', AfilSubGrupo5SinSisbenUpdate.as_view(), name='afil_sub_g5_sin_sisben_edit'),
path('movilidad/list', MovilidadList.as_view(), name='movilidad_list'),
path('movilidad/add', MovilidadCreate.as_view(), name='movilidad_create'),
path('movilidad/edit/<int:pk>', MovilidadUpdate.as_view(), name='movilidad_edit'),
path('segportabilidad/list', SegPortabilidadList.as_view(), name='seg_portabilidad_list'),
path('segportabilidad/add', SegPortabilidadCreate.as_view(), name='seg_portabilidad_create'),
path('segportabilidad/edit/<int:pk>',SegPortabilidadUpdate.as_view(), name='seg_portabilidad_edit'),
path('portabilidad/list', PortabilidadList.as_view(), name='portabilidad_list'),
path('portabilidad/add', PortabilidadCreate.as_view(), name='portabilidad_create'),
path('portabilidad/edit/<int:pk>',PortabilidadUpdate.as_view(), name='portabilidad_edit'),
path('novlcregtipo1/list', NovLcRegTipo1List.as_view(), name='novlcregtipo1_list'),
path('novlcregtipo1/add', NovLcRegTipo1Create.as_view(), name='novlcregtipo1_create'),
path('novlcregtipo1/edit/<int:pk>',NovLcRegTipo1Update.as_view(), name='novlcregtipo1_edit'),
path('delete/novlcregtipo2/<int:pk>', delete_novlcregtipo2, name='delete_novlcregtipo2'),
path('delete/novlcregtipo3/<int:pk>', delete_novlcregtipo3, name='delete_novlcregtipo3'),
path('delete/novlcregtipo4/<int:pk>', delete_novlcregtipo4, name='delete_novlcregtipo4'),
path('delete/novlcregtipo5/<int:pk>', delete_novlcregtipo5, name='delete_novlcregtipo5'),
path('delete/novlcregtipo6/<int:pk>', delete_novlcregtipo6, name='delete_novlcregtipo6'),
path('delete/novlcregtipo7/<int:pk>', delete_novlcregtipo7, name='delete_novlcregtipo7'),
path('delete/novlcregtipo8/<int:pk>', delete_novlcregtipo8, name='delete_novlcregtipo8'),
path('delete/novlcregtipo9/<int:pk>', delete_novlcregtipo9, name='delete_novlcregtipo9'),
path('delete/novlcregtipo10/<int:pk>', delete_novlcregtipo10, name='delete_novlcregtipo10'),
path('delete/novlcregtipo11/<int:pk>', delete_novlcregtipo11, name='delete_novlcregtipo11'),
path('delete/novlcregtipo12/<int:pk>', delete_novlcregtipo12, name='delete_novlcregtipo12'),
path('Rep/novlctxt/<int:id>', report_novedadlc_csv_view, name='rep_novlc_txt'),



]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)