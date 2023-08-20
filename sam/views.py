from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory, inlineformset_factory
from cnf.views import Sin_privilegio
from django.views import generic

from .models import Propietario, Establecimiento, ActaEstabEducativo, ItemActaEstabEducativo, \
	TipoActa, Pregunta, ActaEstEduFuncionario, Atiende_ActaEstabEduc
from cnf.models import Tipodoc, Departamento, Municipio
from .forms import PropietarioForm, EstablecimientoForm, ActaEstabEducativoForm, \
      ItemActaEstabEducativoForm, ActaEstEduFuncionarioForm, Atiende_ActaEstabEducForm
# Create your views here.

def homesam(request):
	contexto ={}
	return render(request, 'base/basesam.html', context=contexto)

class PropietarioList(Sin_privilegio, generic.ListView):
    permission_required="sam.view_Propietario"
    model = Propietario
    template_name='sam/propietario_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class PropietarioCreate(LoginRequiredMixin, generic.CreateView):
	model = Propietario
	template_name = 'sam/propietario_form.html'
	context_object_name = 'obj'
	form_class = PropietarioForm
	success_url = reverse_lazy('sam:propietario_list')
	login_url = 'cnf:login'

class PropietarioEdit(LoginRequiredMixin, generic.UpdateView):
	model = Propietario
	template_name = 'sam/propietario_form.html'
	context_object_name = 'obj'
	form_class = PropietarioForm
	success_url = reverse_lazy('sam:propietario_list')
	login_url = 'cnf:login'  

	def get_context_data(self, **kwargs):
		pk = self.kwargs.get('pk')
		context = super(PropietarioEdit,self).get_context_data(**kwargs)
		context['obj'] = Propietario.objects.filter(pk=pk).first()            
		return context  

class EstablecimientoList(Sin_privilegio, generic.ListView):
    permission_required="sam.view_Establecimiento"
    model = Establecimiento
    template_name='sam/establecimiento_list.html'
    context_object_name = "obj"
    login_url = 'cnf:login'

class EstablecimientoCreate(LoginRequiredMixin, generic.CreateView):
	model = Establecimiento
	template_name = 'sam/establecimiento_form.html'
	context_object_name = 'obj'
	form_class = EstablecimientoForm
	success_url = reverse_lazy('sam:establecimiento_list')
	login_url = 'cnf:login'

	def form_valid(self, form):
		form.instance.uc = self.request.user 
		print(form)
		return super().form_valid(form)
	
	def get_context_data(self, **kwargs):
		context = super(EstablecimientoCreate,self).get_context_data(**kwargs)
		#replegal = Propietario.objects.all()
		dptonot = Departamento.objects.all()
		mpionot = Municipio.objects.all()
		context['dptonot'] = dptonot
		context['mpionot'] = mpionot	
		#context['replegal'] = replegal
		return context

class EstablecimientoEdit(LoginRequiredMixin, generic.UpdateView):
	model = Establecimiento
	template_name = 'sam/establecimiento_form.html'
	context_object_name = 'obj'
	form_class = EstablecimientoForm
	success_url = reverse_lazy('sam:establecimiento_list')
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		context = super(EstablecimientoEdit,self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk') # El mismo nombre que en tu URL		
		iddptonot = self.kwargs.get('dptonotifica') # El mismo nombre que en tu URL		
		idmpionot = self.kwargs.get('mpionotifica') # El mismo nombre que en tu URL		
		idreplegal = self.kwargs.get('replegal') # El mismo nombre que en tu URL	
		#replegal = Propietario.objects.all()
		dptonot = Departamento.objects.all()
		mpionot = Municipio.objects.all()
		context['dptonot'] = dptonot
		context['mpionot'] = mpionot	
		#context['replegal'] = replegal
		context['iddptonot'] = iddptonot
		context['idmpionot'] = idmpionot	
		context['idreplegal'] = idreplegal
		return context

class EstablecimientoEducativoList(Sin_privilegio, generic.ListView):
	permission_required="sam.view_ActaEstabEducativo"
	model = ActaEstabEducativo
	template_name='sam/actaesteducativo_list.html'
	context_object_name = "obj"
	login_url = 'cnf:login'

	def get_context_data(self, **kwargs):
		pk = self.kwargs.get('pk')
		context = super(EstablecimientoEducativoList,self).get_context_data(**kwargs)
		estaeduca = ActaEstabEducativo.objects.filter(establecimiento_id=pk)
		establecimiento = Establecimiento.objects.filter(id=pk).first()
		context['obj'] =estaeduca
		context['idestablecimiento'] = pk
		context['nomestablecimiento'] = establecimiento.razonsocial		
		print(establecimiento.razonsocial)
		return context
 
def establecimientoEducativoCreate(request, estaedu_id, idacta=None):
	
	template_name='sam/actaesteducativo_form.html'
	contexto={}

	if request.method == 'POST':
		if idacta == None:
			form = ActaEstabEducativoForm(request.POST or None)
		else:
			actaestaeducativo = ActaEstabEducativo.objects.get(pk=idacta)
			form = ActaEstabEducativoForm(request.POST, instance=actaestaeducativo)
			print('ingreso con acta creada para actualizar')

		itemactaesteduFormset = inlineformset_factory(ActaEstabEducativo, ItemActaEstabEducativo,form=ItemActaEstabEducativoForm, extra=1)
		funcionariosFormset = inlineformset_factory(ActaEstabEducativo, ActaEstEduFuncionario,form=ActaEstEduFuncionarioForm, extra=2)
		atiende_ActaEstabEducFormset=inlineformset_factory(ActaEstabEducativo, Atiende_ActaEstabEduc,form=Atiende_ActaEstabEducForm, extra=2)

		if idacta == None:
			if form.is_valid():
				actaestaeducativo = form.save()
		else:
			if form.is_valid():
				form.save()

		formsetitem = itemactaesteduFormset(request.POST, instance=actaestaeducativo)
		formsetfuncionario = funcionariosFormset(request.POST, instance=actaestaeducativo)
		formsetatiendeactaestabeduc = atiende_ActaEstabEducFormset(request.POST, instance=actaestaeducativo)

		if formsetitem.is_valid():
			formsetitem.save()

		if formsetfuncionario.is_valid():
			formsetfuncionario.save()

		if formsetatiendeactaestabeduc.is_valid():
			formsetatiendeactaestabeduc.save()


		return redirect('sam:actaestedu_list', pk=estaedu_id)	

	if request.method == 'GET':
		if idacta == None:
			actablanco = ActaEstabEducativo()
			actablanco.establecimiento_id = estaedu_id
			listapreguntas=[]

			tipoacta = TipoActa.objects.filter(idtipoacta='MISFO001').first()
			preguntas = Pregunta.objects.filter(bloque__tipoacta_id=tipoacta.pk)
			for p in preguntas:
				diccitemacta = {
					'actaestabeducativo':actablanco.id,
					'pregunta':p.id,
					'evaluacion':3,
					'hallazgo':'',
					'puntaje':0,
					'habilitada':p.habilitada
				}
				if p.habilitada == False:
					print('Bloque',p.bloque)

				listapreguntas.append(diccitemacta)

			form = ActaEstabEducativoForm(instance=actablanco)
			itemformset = inlineformset_factory(ActaEstabEducativo, ItemActaEstabEducativo,form=ItemActaEstabEducativoForm, 
				extra=len(listapreguntas), can_delete=False)
			formset = itemformset()
			for subform, data in zip(formset.forms, listapreguntas):
				subform.initial = data

			funcionariosFormset = inlineformset_factory(ActaEstabEducativo, ActaEstEduFuncionario, 
				form=ActaEstEduFuncionarioForm, extra=2)
			formsetfuncionario = funcionariosFormset()

			atiende_ActaEstabEducFormset=inlineformset_factory(ActaEstabEducativo, Atiende_ActaEstabEduc, 
				form=Atiende_ActaEstabEducForm, extra=2)

			formsetatiendeactaestabeduc = atiende_ActaEstabEducFormset()

			contexto={'form':form, 'formset':formset, 'formsetfunc':formsetfuncionario, 'formsetatiende':formsetatiendeactaestabeduc, 'establecimiento_id':estaedu_id} 
		else:
			actaestabeducativo = ActaEstabEducativo.objects.get(pk=idacta)
			form = ActaEstabEducativoForm(instance=actaestabeducativo)
			itemformset = inlineformset_factory(ActaEstabEducativo, ItemActaEstabEducativo,form=ItemActaEstabEducativoForm, \
				extra=0, can_delete=False)
			formset = itemformset(instance=actaestabeducativo)

			funcionariosFormset = inlineformset_factory(ActaEstabEducativo, ActaEstEduFuncionario, form=ActaEstEduFuncionarioForm, extra=2)
			formsetfuncionario = funcionariosFormset(instance=actaestabeducativo) 
			
			atiende_ActaEstabEducFormset=inlineformset_factory(ActaEstabEducativo, Atiende_ActaEstabEduc, 
				  form=Atiende_ActaEstabEducForm, extra=2)
			formsetatiendeactaestabeduc = atiende_ActaEstabEducFormset(instance=actaestabeducativo)

			contexto={'form':form, 'formset':formset, 'formsetfunc':formsetfuncionario, 'formsetatiende':formsetatiendeactaestabeduc, 'establecimiento_id':estaedu_id, 'idacta':idacta, 'obj':actaestabeducativo} 
		return render(request, template_name, contexto)
	return render(request, template_name, contexto)

