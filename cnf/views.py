import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Paciente, Ocupacion, Departamento, Municipio, Comuna, Barrio, \
    Pais
from .forms import PacienteForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mpl_toolkits.basemap.test import Basemap
from geopy.geocoders import Nominatim
import time
import math



import pandas as pd
# Create your views here.


#Vistas para renderizar simple

class Sin_privilegio(LoginRequiredMixin, PermissionRequiredMixin):
	login_url = 'cnf:login'
	raise_exception=False
	redirect_field_name = "redirect_to"

	def handle_no_permission(self):
		from django.contrib.auth.models import AnonymousUser
		if not self.request.user== AnonymousUser():
			self.login_url="cnf:sin_privilegios"
		return HttpResponseRedirect(reverse_lazy(self.login_url))

class pacienteListView(Sin_privilegio, generic.ListView):
    permission_required="cnf.view_paciente"
    model = Paciente
    context_object_name = "obj"
    template_name='cnf/paciente_list_ajax.html'
    login_url = 'cnf:login'

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            pacientes = Paciente.objects.filter(estado=True)
            action = request.POST['action']
            if action == "searchdata":
                data = []                
                for pac in pacientes:
                    data.append(pac.toJson())
            else:
                data['error'] = 'Ha ocurrido  un error'

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class PacienteView(Sin_privilegio, generic.TemplateView):
    permission_required="cnf.view_paciente"
    template_name='cnf/paciente_list_reload.html'


def listadopacientereload(request):
    context = {}
    dt = request.GET

    draw = int(dt.get("draw"))
    start = int(dt.get("start"))
    length = int(dt.get("length"))
    search = dt.get("search[value]")
    
    registros = Paciente.objects.all().values("id","tipodoc__codigo","identificacion","razonsocial","direccion", "telefono","eps__descripcion", \
         "estado").order_by("id")
   
    if search:
        registros = registros.filter(            
            Q(identificacion__icontains=search) |
            Q(razonsocial__icontains=search) |
            Q(eps__descripcion__icontains=search) |         
            Q(estado__icontains=search)
            )
    
    recordsTotal = registros.count()
    recordsFiltered = recordsTotal
    #preparamos la salida
    context["draw"] = draw
    context["recordsTotal"] = recordsTotal
    context["recordsFiltered"] = recordsFiltered

    reg = registros[start:start + length]
    
    paginator = Paginator(reg, length)
    try:
        obj = paginator.page(draw).object_list
    except PageNotAnInteger:
        obj = paginator.page(draw).object_list
    except:
        obj = paginator.page(paginator.num_pages).object_list

    datos = [
        {       
        "id":d['id'],
        "tipodoc__codigo":d['tipodoc__codigo'],        
        "identificacion":d['identificacion'],
        "razonsocial":d['razonsocial'],
        "direccion":d['direccion'],
        "telefono":d['telefono'],
        "eps__descripcion":d['eps__descripcion'],
        "estado":d['estado']
        } for d in obj
    ]

    context["datos"] = datos 
    return JsonResponse(context,safe=False)

def obtener_lat_lon(direcc):
    latlong = {'lat':'SD', 'lon':'SD'}
    print(direcc)
    if (direcc != '') and (direcc != None) :
        if direcc.strip() != '':
            geo = Nominatim(user_agent='MyApp', timeout=10)
            direcc = direcc.lower()
            loc = geo.geocode(direcc, timeout=10)   
            print("Detecto coordenadas:", loc)    
            if loc:             
                latlong ={'lat':loc.latitude, 'lon':loc.longitude}

    return latlong


class PacienteEdit(LoginRequiredMixin, generic.UpdateView):
    model = Paciente
    template_name = 'cnf/paciente_form.html'
    context_object_name = 'obj'
    form_class = PacienteForm
    success_url = reverse_lazy('cnf:paciente_list')
    login_url = 'cnf:login'  

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')       
        context = super(PacienteEdit,self).get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['municipios'] = Municipio.objects.all()             
        context['barrios'] = Barrio.objects.all()
        context['obj'] = Paciente.objects.filter(pk=pk).first()            
        return context  

    def form_valid(self, form):
        direcc = form.instance.direccion
        latlong = obtener_lat_lon(form.cleaned_data.get('direccion'))
        print('Latitud: ',latlong['lat'])

        if latlong['lat'] != 'SD':
            form.instance.lat = latlong['lat']
        if  latlong['lon'] != 'SD':
            form.instance.lon = latlong['lon']
        return super().form_valid(form) 


class PacienteCreate(LoginRequiredMixin, generic.CreateView):
    model = Paciente
    template_name = 'cnf/paciente_form.html'
    context_object_name = 'obj'
    form_class = PacienteForm
    success_url = reverse_lazy('cnf:paciente_list')
    login_url = 'cnf:login'

    def get_initial(self):
        initial = super().get_initial()
        initial['pais'] = Pais.objects.filter(nacional=True).first()
        return initial 


    def form_valid(self, form):
        form.instance.uc = self.request.user
        latitud = form.instance.lat
        print("Latidud:",latitud)
        if (latitud.strip()=='') or (latitud.strip()=='SD'):
            if form.instance.direccion != '':
                if form.instance.strip() != '':
                    geo = Nominatim(user_agent='MyApp', timeout=5)
                    direcc = form.instance.lower()
                    loc = geo.geocode(direcc, timeout=5)                    
                    form.instance.lat = loc.latitude
                    form.instance.lon = loc.longitude
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        context = super(PacienteCreate,self).get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['municipios'] = Municipio.objects.all()      
        context['barrios'] = Barrio.objects.all()  
          
        return context 

  

class PacienteAjaxCreate(LoginRequiredMixin, generic.CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'cnf/paciente_form_ajax.html'
    context_object_name = 'obj'
    login_url = 'cnf:login'
    #success_url = reverse_lazy('cnf:paciente_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.is_ajax():            
            if form.is_valid():
                nuevopac = Paciente(
                    tipodoc = form.cleaned_data.get('tipodoc'),
                    identificacion = form.cleaned_data.get('identificacion'),
                    nombre1 = form.cleaned_data.get('nombre1'),
                    nombre2 = form.cleaned_data.get('nombre2'),
                    apellido1 = form.cleaned_data.get('apellido1'),
                    apellido2 = form.cleaned_data.get('apellido2'),
                    fechaNac = form.cleaned_data.get('fechaNac'),
                    departamento = form.cleaned_data.get('departamento'),
                    municipio = form.cleaned_data.get('municipio'),
                    direccion = form.cleaned_data.get('direccion'),
                    telefono = form.cleaned_data.get('telefono'),
                    correoelectronico = form.cleaned_data.get('correoelectronico'),
                    barrio = form.cleaned_data.get('barrio'),
                    area = form.cleaned_data.get('area'),
                    regimen = form.cleaned_data.get('regimen'),
                    eps = form.cleaned_data.get('eps'),
                    sexo = form.cleaned_data.get('sexo'),
                    etnia = form.cleaned_data.get('etnia'),
                    latlong = obtener_lat_lon(form.cleaned_data.get('direccion')),        
                    lat = latlong['lat'],
                    lon = latlong['long']
                    )
                nuevopac.save()
                mensaje = 'Paciente registrado correctamente'
                error = 'No hay error'
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 201
                return response
            else:
                nuevopac.save()
                mensaje = 'Se presento un error el Paciente No se ha podido registrar'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('cnf:paciente_list')

    def form_valid(self, form):
        form.instance.uc = self.request.user 
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        context = super(PacienteAjaxCreate,self).get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['municipios'] = Municipio.objects.all()             
        return context
    def get_initial(self):
        initial = super().get_initial()
        initial['pais'] = Pais.objects.filter(nacional=True).first()
        return initial 

def load_barrios(request):
    municipio_id = request.GET.get('idmunicipio')
    barrios = Barrio.objects.filter(comuna__municipio_id=municipio_id).order_by('descripcion')
    return render(request, 'cnf/barrio_dropdown_list_options.html', {'barrios': barrios})


def inactivarPaciente(request, id):
    paciente = Paciente.objects.filter(pk=id).first()
    if request.method == 'POST':
        if paciente:
            paciente.estado = not paciente.estado
            paciente.save()
            return HttpResponse('OK')
        else:
            return HttpResponse('FAIL')
    
    return HttpResponse('FAIL')


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'cnf/index.html'
    login_url='cnf:login'


class HomeSinPrivilegio(generic.TemplateView):
	template_name = 'base/sin_privilegios.html'
