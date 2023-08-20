import folium
from folium.plugins import MarkerCluster
import pandas as pd 
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from cnf.models import Paciente
import webbrowser


# Create your views here.
from .models import Sintomatico
from cnf.views import Sin_privilegio
from .forms import SintomaticoForm 



class Principal(Sin_privilegio, generic.TemplateView):
	permission_required="sint.view_sintomatico"	
	template_name='base/basetb.html'


class GrafSintomas(generic.TemplateView):
	template_name='sint/estsintomaticos_form.html'

	def cantsintoma(self, id):
		#anio = datetime.now().year
		data=[]		
		if id==1:
			sint = Sintomatico.objects.filter(fiebre='SI').count()
		if id==2:
			sint = Sintomatico.objects.filter(cefalea='SI').count()
		if id==3:
			sint = Sintomatico.objects.filter(doloretrocular='SI').count()
		if id==4:
			sint = Sintomatico.objects.filter(mialgias='SI').count()
		if id==5:
			sint = Sintomatico.objects.filter(artralgias='SI').count()
		if id==6:
			sint = Sintomatico.objects.filter(rash='SI').count()
		if id==7:
			sint = Sintomatico.objects.filter(zona_endemica_dengue='SI').count()
		if id==8:
			sint = Sintomatico.objects.filter(tos='SI').count()
		if id==9:
			sint = Sintomatico.objects.filter(perdida_peso='SI').count()
		if id==10:
			sint = Sintomatico.objects.filter(sudor_nocturna='SI').count()


		data.append(float(sint))		
		return data
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['panel']='Panel de Administrador'
	    context['fiebre']=self.cantsintoma(1)
	    context['cefalea']=self.cantsintoma(2)
	    context['doloretrocular']=self.cantsintoma(3)
	    context['mialgias']=self.cantsintoma(4)
	    context['artralgias']=self.cantsintoma(5)
	    context['rash']=self.cantsintoma(6)
	    context['zona_endemica_dengue']=self.cantsintoma(7)
	    context['tos']=self.cantsintoma(8)
	    context['perdida_peso']=self.cantsintoma(9)
	    context['sudor_nocturna']=self.cantsintoma(10)
	    return context

class SintomaticoList(Sin_privilegio, generic.ListView):
    permission_required="sint.view_sintomatico"
    model = Sintomatico
    template_name='sint/sintomatico_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'


class SintomaticoEdit(Sin_privilegio, generic.UpdateView):
	permission_required="sint.change_sintomatico"
	model=Sintomatico	
	template_name = 'sint/sintomatico_form.html'
	context_object_name = 'obj'
	form_class = SintomaticoForm
	success_url = reverse_lazy('sint:sintomatico_list')
	login_url = 'cnf:login'


class SintomaticoCreate(Sin_privilegio, generic.CreateView):
	permission_required="sint.add_sintomatico"
	model = Sintomatico
	template_name = 'sint/sintomatico_form.html'
	context_object_name = 'obj'
	form_class = SintomaticoForm
	success_url = reverse_lazy('sint:sintomatico_list')
	login_url = 'cnf:login'    

	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form) 

def geolocDetallado(request):
	
	pacientes = Paciente.objects.filter(~Q(lat='SD')).filter(~Q(lon='SD'))
	
	some_map = folium.Map(location=[3.3826111,-76.5419858], zoom_start = 10)
	
	for row in pacientes:
		some_map.add_child(folium.Marker(location=[row.lat, row.lon], popup=row.identificacion))

	filepath = 'C:/mapas/mapa.html'
	some_map.save(filepath)
	webbrowser.open('file://' + filepath)


	
	html_string = some_map.get_root().render()
	context = {'sm':some_map, 'pac':pacientes, 'hs':html_string}

	return redirect('sint:sintomatico_list')

def geolocMapaCalor(request):
	pacientes = Paciente.objects.filter(~Q(lat='SD')).filter(~Q(lon='SD'))
	
	some_map2 = folium.Map(location=[3.3826111,-76.5419858], zoom_start = 10)
	mc = MarkerCluster()


	for row in pacientes:
		if not row.lat == 'SD': 
			mc.add_child(folium.Marker(location=[row.lat, row.lon], popup=row.identificacion))

	some_map2.add_child(mc)

	filepath = 'C:/mapas/mapacalor.html'
	some_map2.save(filepath)
	webbrowser.open('file://' + filepath)

	html_string = some_map2.get_root().render()
	context = {'sm':some_map2, 'pac':pacientes, 'hs':html_string}

	return redirect('sint:sintomatico_list')


	

