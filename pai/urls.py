from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import importarRediarios, RediarioList, GrafLaborartio, GrafVacunaIps, \
GrafPaiDosisAplicadas, RediarioCreate, RediarioUpdate, RediarioListAjax, RediarioPrint, \
GrafVacunaModalidad, GrafVacunaEtapa, GrafTipoPoblacion, GrafTipoSexo, PrincipalPai, \
importarRediariosPaiRegular, listar_rediario_regular


app_name='pai'

urlpatterns = [
path('', PrincipalPai.as_view(), name='home'),
path('rediario/import', importarRediarios, name='importar_rediarios'),
path('red/import/paireg', importarRediariosPaiRegular, name='import_red_pai_reg'),
path('rediario/reg/list', listar_rediario_regular, name='rediario_reg_list'),

path('rediario/list/', RediarioList.as_view(), name='rediario_list'),
path('rediario/print/<int:id>', RediarioPrint.as_view(), name='Imprimir_datos_vacuna'),
path('rediario/search/<str:dato>', RediarioListAjax.as_view(), name='rediario_search'),
path('rediario/create', RediarioCreate.as_view(), name='rediario_new'),
path('rediario/update/<int:pk>', RediarioUpdate.as_view(), name='rediario_edit'),
path('estadistica/lab', GrafLaborartio.as_view(), name='estlaboratorio'),
path('estadistica/ips', GrafVacunaIps.as_view(), name='estips'),
path('estadistica/modalidad', GrafVacunaModalidad.as_view(), name='estmodalidad'),
path('estadistica/nrodosis', GrafPaiDosisAplicadas.as_view(), name='estnrodosis'),
path('estadistica/etapa', GrafVacunaEtapa.as_view(), name='estapa'),
path('estadistica/tipob', GrafTipoPoblacion.as_view(), name='tipo_poblacion'),
path('estadistica/sexo', GrafTipoSexo.as_view(), name='tipo_sexo'),





#path('propietario', PropietarioList.as_view(), name='propietario_list'),

]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)