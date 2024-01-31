from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
#from django.conf.urls import url
from cnf.views import Sin_privilegio
from django.views import generic

from .views import BacList, BacCreate, BacEdit, FichaIecList, FichaIecCreate, FichaIecEdit, \
AntecedenteViajeCreate, SeguimientoIecList, SeguimientoIecNew, SeguimientoIecedit, tareasSegIec, \
ConglomeradoList, ConglomeradoCreate, ConglomeradoEdit, geolocConglomerado, importarCovid19, \
notifCovidList, SeguimientoNotifCovid, anexos_fichaIec, AntecedenteViajeUpdate, \
AntecHospitalizacionCreate, AntecHospitalizacionUpdate, FileIecList, FileIecCreate, FileIecUpdate, \
ContactoIecCreate, ContactoIecUpdate, ContactoIecList, contactoIecDetail, DesplazaContactoCreate, \
DesplazaContactoUpdate, SeguimientoContactoCreate, SeguimientoContactoUpdate, GrafCovidSemEpi, \
inactivarNotifPaconglemerado, NotifPaConglomeradoList, NotifPaConglomeradoCreate, NotifPaConglomeradoUpdate, \
ContactoAisladoCreate, ContactoAisladoUpdate, SegContactoAisladoCreate, SegContactoAisladoUpdate, \
ConfigConglomeradoList, ConfigConglomeradoCreate, ConfigConglomeradoUpdate, GrafSintomasCovid, \
GrafCovidBarrio, GrafCoomorbCovid, geolocFichasIEC, PacienteCreate,createNewPac, busqpaciente, \
PrincipalCovid, notifCovidEdit, SeguimientoNotifCovidUpdate


from .reportes import imprimir_tareas_list, ReporteCuadroMando, ReportConglomerado, RepConglomerado

app_name='cvd'

urlpatterns = [

    path('', PrincipalCovid.as_view(), name='home'),
    path('baclist', BacList.as_view(), name='bac_list'),
    path('bac/new', BacCreate.as_view(), name='bac_new'),
    path('bac/edit/<int:pk>', BacEdit.as_view(), name='bac_edit'),
    path('iec', FichaIecList.as_view(), name='iec_list'),
    path('iec/new', FichaIecCreate.as_view(), name='iec_new'),
    path('iec/edit/<int:pk>', FichaIecEdit.as_view(), name='iec_edit'),
    path('iec/contacto/new/<int:idficha>',ContactoIecCreate.as_view(), name='contactoiec_new'),
    path('iec/contacto/edit/<int:pk>', ContactoIecUpdate.as_view(), name='contactoiec_edit'),
    path('iec/verfichaiec/<int:id>', anexos_fichaIec, name='ver_fichaiec'),
    path('iec/antviaje/new/<int:idficha>',AntecedenteViajeCreate.as_view(), name='iec_viaje_new'),
    path('iec/antviaje/edit/<int:pk>', AntecedenteViajeUpdate.as_view(), name='iec_viaje_edit'),
    path('iec/anthosp/new/<int:idficha>', AntecHospitalizacionCreate.as_view(), name='iec_anthosp_new'),
    path('iec/anthosp/edit/<int:pk>', AntecHospitalizacionUpdate.as_view(), name='iec_anthosp_edit'),
    path('iec/seg', SeguimientoIecList.as_view(), name='iec_seguimiento_list'),
    path('iec/seg/new', SeguimientoIecNew.as_view(), name='iec_seguimiento_new'),
    path('iec/seg/edit/<int:pk>', SeguimientoIecedit.as_view(), name='iec_seguimiento_edit'),
    path('iec/tareas', tareasSegIec, name='iec_tareas_list'),
    path('iec/imprimir-todas/<str:f1>/<str:f2>', imprimir_tareas_list, name='iec_tareas_print_all'),
    path('iec/conglomerado', ConglomeradoList.as_view(), name='conglomerado_list'),
    path('iec/conglomerado/new', ConglomeradoCreate.as_view(), name='conglomerado_new'),
    path('iec/conglomerado/edit/<int:pk>', ConglomeradoEdit.as_view(), name='conglomerado_edit'),
    path('iec/conglomerado/geoloc', geolocConglomerado, name='geoloc_conglomerado'),
    path('iec/fileiec', FileIecList.as_view(), name='fileiec_list'),
    path('iec/fileiec/new/<int:idficha>', FileIecCreate.as_view(), name='fileiec_new'),
    path('iec/fileiec/edit/<int:pk>', FileIecUpdate.as_view(), name='fileiec_edit'),
    path('iec/repcuadromando', ReporteCuadroMando.as_view(), name='cuadro_mando_rep'),
    path('iec/contacto', ContactoIecList.as_view(), name='contacto_list'),
    path('iec/contacto/detalle/<int:id>', contactoIecDetail, name='contacto_detalle'),        
    path('iec/contacto/desp/new/<int:id>', DesplazaContactoCreate.as_view(), name='desplacontacto_new'),        
    path('iec/contacto/desp/edit/<int:pk>', DesplazaContactoUpdate.as_view(), name='desplacontacto_edit'),        
    path('iec/contacto/seg/new/<int:id>', SeguimientoContactoCreate.as_view(), name='seguimientocontacto_new'),        
    path('iec/contacto/seg/edit/<int:pk>', SeguimientoContactoUpdate.as_view(), name='seguimientocontacto_edit'),        
    path('iec/graf/cvd/', GrafCovidSemEpi.as_view(), name='estadisticacovid_sem'),      
    path('import/sivigila', importarCovid19, name='import_covid'),
    path('sivcovid/list', notifCovidList, name='notif_covid_sivigila_list'),
    path('sivcovid/ver/<int:id>', notifCovidEdit, name='notif_covid_sivigila_ver'),
    path('sivcovid/seg/<int:idnotif>', SeguimientoNotifCovid.as_view(), name='seg_notif_covid_add'),    
    path('sivcovid/seg/upt/<int:pk>', SeguimientoNotifCovidUpdate.as_view(), name='seg_notif_covid_change'),    

    path('con/emp/notifpac/<int:id>', inactivarNotifPaconglemerado, name='paconglomerado_inactivar'),
    path('con/emp/notifpac/list', NotifPaConglomeradoList.as_view(), name='paconglomerado_list'),
    path('con/emp/notifpac/new', NotifPaConglomeradoCreate.as_view(), name='paconglomerado_new'),
    path('con/emp/notifpac/edit/<int:pk>', NotifPaConglomeradoUpdate.as_view(), name='paconglomerado_edit'),
    path('con/emp/conotifpac/new/<int:id>', ContactoAisladoCreate.as_view(), name='contactopacnotif_new'),
    path('con/emp/conotifpac/edit/<int:pk>', ContactoAisladoUpdate.as_view(), name='contactopacnotif_edit'),
    path('con/emp/Segconotifpac/new/<int:id>', SegContactoAisladoCreate.as_view(), name='segcontactopacnotif_new'),
    path('con/emp/segconotifpac/edit/<int:pk>', SegContactoAisladoUpdate.as_view(), name='segcontactopacnotif_edit'),
    path('iec/confconglo/list', ConfigConglomeradoList.as_view(), name='config_conglomerado_list'),
    path('iec/confconglo/new', ConfigConglomeradoCreate.as_view(), name='config_conglomerado_new'),
    path('iec/confconglo/edit/<int:pk>', ConfigConglomeradoUpdate.as_view(), name='config_conglomerado_edit'),
    path('iec/repconglo', ReportConglomerado.as_view(), name='conglomerado_report'),
    path('iec/reponeconglo/<int:pk>', RepConglomerado.as_view(), name='reporte_conglomerado'),
    path('iec/paciente', createNewPac, name='paciente_new'),     
    path('iec/estadsintomacovid', GrafSintomasCovid.as_view(), name='sintomas_covid_est'),
    path('iec/estadcovidbarrio', GrafCovidBarrio.as_view(), name='paccovid_barrio_est'),
    path('iec/estadcovidcoom', GrafCoomorbCovid.as_view(), name='paccovid_coomorbilidad_est'),
    path('iec/geoloc', geolocFichasIEC, name='geoloc_iec'),
    path('pac/busq', busqpaciente, name='busqpac'),

    
] 

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)