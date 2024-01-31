from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count


from cnf.views import Sin_privilegio
from .models import Pqrs, SeguimientoPQRS
from .forms import PqrsForm, SegPqrsFormSet, ReportPqrsForm

# Create your views here.

class PrincipalPqrs(Sin_privilegio, generic.TemplateView):
	permission_required="pqrs.view_pqrs"	
	template_name='base/basepqrs.html'

class PqrsList(Sin_privilegio, generic.ListView):
	permission_required="pqrs.view_pqrs"	
	model = Pqrs
	template_name='pqrs/pqrs_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'


class PqrsInline():
	form_class = PqrsForm	
	model = Pqrs
	template_name = 'pqrs/pqrs_form.html'

	def form_valid(self, form):		
		named_formsets = self.get_named_formsets()
		if not all((x.is_valid() for x in named_formsets.values())):
			return self.render_to_response(self.get_context_data(form=form))

		self.object = form.save()

		for name, formset in named_formsets.items():
			formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
			if formset_save_func is not None:				
				formset_save_func(formset)
			else:
				formset.save()

		return redirect('pqrs:pqrs_list')
		#print(form.instance)
		#return super().form_valid(form)
	
	def formset_seguimientopqrs_valid(self, formset):		
		segpqrs = formset.save(commit=False)  # self.save_formset(formset, contact)
		for obj in formset.deleted_objects:
			obj.delete()

		for seg in segpqrs:
			seg.pqrs = self.object
			seg.save()



def delete_seguimiento_pqrs(request, pk):
	try:
		segpqrs = SeguimientoPQRS.objects.get(id=pk)
	except SeguimientoPQRS.DoesNotExist:
		messages.success(
			request, 'Seguimiento PQRS no existe'
			)
		return redirect('pqrs:pqrs_edit', pk=segpqrs.pqrs.id)

	segpqrs.delete()
	messages.success(
		request, 'Seguimiento Eliminado satisfactoria mente'
		)
	return redirect('pqrs:pqrs_edit', pk=segpqrs.pqrs.id)


class PqrsCreate(Sin_privilegio, PqrsInline, generic.CreateView):
	permission_required="pqrs.add_pqrs"
	#context_object_name = 'obj'
	#success_url = reverse_lazy('pqrs:pqrs_list')		
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		ctx = super(PqrsCreate, self).get_context_data(**kwargs)
		ctx['named_formsets'] = self.get_named_formsets()
		return ctx

	def get_named_formsets(self):
		if self.request.method == "GET":
			return {
                'seguimientopqrs': SegPqrsFormSet(prefix='seguimientopqrs')
                #'images': ImageFormSet(prefix='images'),
            }
		else:
			return {
                'seguimientopqrs': SegPqrsFormSet(self.request.POST or None, prefix='seguimientopqrs')
                #'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }

class PqrsUpdate(Sin_privilegio, PqrsInline, generic.UpdateView):
	permission_required="pqrs.change_pqrs"
	#context_object_name = 'obj'
	#success_url = reverse_lazy('pqrs:pqrs_list')		
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		ctx = super(PqrsUpdate, self).get_context_data(**kwargs)
		ctx['named_formsets'] = self.get_named_formsets()
		ctx['obj']=self.object
		return ctx
	
	def get_named_formsets(self):
		return {
		'seguimientopqrs': SegPqrsFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='seguimientopqrs')
		}	

       
#@login_required(login_url="/login/")
#@permission_required("cmp.change_proveedor",login_url="/login/")
def pqrsCreateView(request):
	#template_name='pqrs/pqrs_form.html'
	contexto={}
	form = PqrsForm()
	if request.method == 'POST':
		form = PqrsForm(request.POST)

		if form.is_valid():
			print("Ingresa hasta aqui")
			form.save()
			return redirect('pqrs:pqrs_list')
	return render(request, 'pqrs/pqrs_form.html', {'form': form})



class EstadisticaPqrs(generic.TemplateView):
	template_name='pqrs/estadisticaPQRS.html'

	def estadisticaxEAPB(self):
		diccionario = {}
		data=[]
		datosms = Pqrs.objects.values('eps__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			nameps = x['eps__descripcion']
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				data.append(diccionario)
		return data

	def estadisticaxInstitucion(self):
		diccionario = {}
		data=[]
		datosms = Pqrs.objects.values('pqrscontra').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			nameps = x['pqrscontra']
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				data.append(diccionario)
		return data

	def estadisticaxservicio(self):
		diccionario = {}
		data=[]
		datosms = Pqrs.objects.values('serviciosobjqueja__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			nameps = x['serviciosobjqueja__descripcion']
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				data.append(diccionario)
		return data

	def estadisticaxtiporespuesta(self):
		diccionario = {}
		data=[]
		datosms = Pqrs.objects.filter(respondida=True).values('tiporespuestapqrs__descripcion').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			nameps = x['tiporespuestapqrs__descripcion']
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				data.append(diccionario)
		return data

	def estadisticarespondidas(self):
		diccionario = {}
		data=[]
		datosms = Pqrs.objects.values('respondida').annotate(cant=Count('id'))

		for x in datosms:
			cant = x['cant']
			if x['respondida']:
				nameps = 'SI'
			else:
				nameps = 'NO'
				
			if nameps == None:
				nameps="Sin dato"

			if cant > 0:
				diccionario = {'name':nameps,'y':cant}
				print(diccionario)
				data.append(diccionario)

		return data


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['eps']= self.estadisticaxEAPB()
	    context['tipoinst']= self.estadisticaxInstitucion()
	    context['servicio']= self.estadisticaxservicio()
	    context['tipores']= self.estadisticaxtiporespuesta()  
	    context['respondida']= self.estadisticarespondidas()         
	    return context


class ReportPqrs(Sin_privilegio, generic.TemplateView):
	permission_required="pqrs.view_pqrs"
	template_name = 'pqrs/report_pqrs.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		data= {}
				
		try:			
			action=request.POST.get("action")
			if action == 'search_report':
				data=[]
				
				start_date=request.POST.get('start_date','')
				end_date=request.POST.get('end_date','')
				search =Pqrs.objects.all().values("fecha","paciente__identificacion","paciente__razonsocial",\
				"paciente__direccion","paciente__telefono","pqrscontra","eps__descripcion")
				if len(start_date) and len(end_date):
					search = search.filter(fecha__range=[start_date, end_date])
				for s in search:
					data.append([
							s['fecha'].strftime('%Y-%m-%d'),
							s['paciente__identificacion'],
							s['paciente__razonsocial'],
							s['paciente__direccion'],
							s['paciente__telefono'],
							s['pqrscontra'],
							s['eps__descripcion'],
						])

							
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data[0] = str(e)			
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		context['list_url']= reverse_lazy('pqrs:pqrs_report')
		context['form']=ReportPqrsForm()
		return context


class ReportPqrsActivas(Sin_privilegio, generic.TemplateView):
	permission_required="pqrs.view_pqrs"
	template_name = 'pqrs/report_pqrs.html'


	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		data= {}
				
		try:			
			action=request.POST.get("action")
			if action == 'search_report':
				data=[]
				
				start_date=request.POST.get('start_date','')
				end_date=request.POST.get('end_date','')
				search =Pqrs.objects.all().values("fecha","paciente__identificacion","paciente__razonsocial",\
				"paciente__direccion","paciente__telefono","pqrscontra","eps__descripcion")
				if len(start_date) and len(end_date):
					search = search.filter(respondida=False).filter(fecha__range=[start_date, end_date])
				for s in search:
					data.append([
							s['fecha'].strftime('%Y-%m-%d'),
							s['paciente__identificacion'],
							s['paciente__razonsocial'],
							s['paciente__direccion'],
							s['paciente__telefono'],
							s['pqrscontra'],
							s['eps__descripcion'],
						])

							
			else:
				data['error'] = 'Ha ocurrido un error'
		except Exception as e:
			data[0] = str(e)			
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		context['list_url']= reverse_lazy('pqrs:pqrs_rep_activas')
		context['form']=ReportPqrsForm()
		return context