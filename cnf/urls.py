
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views


from .views import Home, HomeSinPrivilegio, PacienteView, PacienteCreate, PacienteEdit, inactivarPaciente, \
PacienteAjaxCreate, pacienteListView, load_barrios, listadopacientereload

app_name='cnf'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='cnf/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='cnf/login.html'), name='logout'),
    path('sin_privilegios/', HomeSinPrivilegio.as_view(), name='sin_privilegios'),
    path('paciente/', PacienteView.as_view(), name='paciente_list'),
    path('paciente/new', PacienteCreate.as_view(), name='paciente_new'),
    path('paciente/edit/<int:pk>', PacienteEdit.as_view(), name='paciente_edit'),
    path('paciente/estado/<int:id>', inactivarPaciente, name='paciente_inactivar'),
    path('paciente/new/ajax', PacienteAjaxCreate.as_view(), name='paciente_new_ajax'),
    path('paciente/list/', pacienteListView.as_view(), name='paciente_list_ajax'),
    path('ajax/load-barrio/', load_barrios, name='ajax_load_barrio'),
    path('pac/list/', listadopacientereload, name='list_paciente_reload'),

      

]