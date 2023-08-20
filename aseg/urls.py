from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import MaestrobduaList, importarmaestrobdua, Principal, importarmaestrocontributivo, \
	MaestrocontList, MaestroListSS, aseg_reload, dt_serverside, ContributivoListSS, aseg_reload_contributivo, \
	dt_serverside_contributivo

app_name='aseg'

urlpatterns = [
path('maestrobdua/import', importarmaestrobdua, name='importar_maestrobdua'),
path('maestrobdua/list/', MaestrobduaList.as_view(), name='maestrobdua_list'),
path('maestrobdua/listss/', MaestroListSS.as_view(), name='maestrobdua_listss'),
path('maestrobdua/listsub/', aseg_reload, name='listar_subsidiado'),
path('maestrobdua/listss_reload/', dt_serverside, name='listss_reload'),

path('maestrocont/import', importarmaestrocontributivo, name='importar_maestrocont'),
path('maestrocont/list/', ContributivoListSS.as_view(), name='maestrocont_list'),
#path('maestrocont/listcont/', aseg_reload_contributivo, name='listar_contributivo'),
path('maestrocont/listss_reload/', dt_serverside_contributivo, name='listcont_reload'),


path('bdua', Principal.as_view(), name='bdua'),

]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)