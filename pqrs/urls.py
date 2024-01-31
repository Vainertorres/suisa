from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from cnf.views import Sin_privilegio
from django.views import generic

from .views import PrincipalPqrs, PqrsList, PqrsCreate, PqrsUpdate, pqrsCreateView, \
delete_seguimiento_pqrs, EstadisticaPqrs, ReportPqrs, ReportPqrsActivas


app_name='pqrs'

urlpatterns = [
path('', PrincipalPqrs.as_view(), name='home'),
path('listpqrs', PqrsList.as_view(), name='pqrs_list'),
path('add/pqrs', PqrsCreate.as_view(), name='pqrs_new'),
path('change/pqrs/<int:pk>', PqrsUpdate.as_view(), name='pqrs_edit'),
path('delete/seg/<int:pk>', delete_seguimiento_pqrs, name='delete_seguimiento'),
path('estadistica', EstadisticaPqrs.as_view(), name='pqrs_estadistica'),
path('report', ReportPqrs.as_view(), name='pqrs_report'),
path('repqrs/activas', ReportPqrsActivas.as_view(), name='pqrs_rep_activas'),



]

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)