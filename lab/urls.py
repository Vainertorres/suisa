from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import RepLaboratorioList, RepLaboratorioCreate, RepLaboratorioUpdate

app_name='lab'

urlpatterns = [
path('lab/replab/list', RepLaboratorioList.as_view(), name='reportelab_list'),
path('lab/replab/new', RepLaboratorioCreate.as_view(), name='reportelab_new'),
path('lab/replab/edit/<int:pk>', RepLaboratorioUpdate.as_view(), name='reportelab_edit'),
]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)