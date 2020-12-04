from django.shortcuts import render,redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.UnidadOrganizacional.models import UnidadOrganizacional
from apps.UnidadOrganizacional.forms import unidad_form
import json

class UnidadList(ListView):
    model=UnidadOrganizacional
    template_name='unidad/index_unidad.html'


#Vista para guardar las solicitudes
class UnidadCreate(CreateView):
    model=UnidadOrganizacional
    template_name='unidad/form_unidad.html'
    form_class=unidad_form
    success_url=reverse_lazy('index unidad') #Para que nos devuelva a la lista
    
    def get_context_data(self, **kwargs):
        context=super(UnidadCreate, self).get_context_data(**kwargs)
        #Le mandamos el formulario en el context
        if 'form' not in context:
            #Se agrega el formulario al contexto
            context['form']=self.form_class(self.request.GET)
        return context
    
    #Para guardar los datos y crear la relacion con el modelo
    def post(self, request, *arg, **kwargs):
        self.object = self.get_object
        #Tomamos del formulario la informacion registrada
        form=self.form_class(request.POST)
        if form.is_valid():
            #Aca guardamos los request del formulario
            solicitud=form.save()
            solicitud.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UnidadUpdate(UpdateView):
    model=UnidadOrganizacional
    template_name='unidad/form_unidad.html'
    form_class=unidad_form
    success_url=reverse_lazy('index unidad')
    

    def get_context_data(self, **kwargs):
        #Aca llamamos a los objetos y que se rendericen en cada texto de nuestro update y asi llenar el form
        context=super(UnidadUpdate, self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        solicitud=self.model.objects.get(idUnidad=pk)
        if  'form' not in context:
            context['form']=self.form_class()
        context['id']=pk
        return context



#id_unidad nos sirve para referenciar al objeto que eliminamos
def UnidadDelete(request, id_unidad):
    unidad = UnidadOrganizacional.objects.get(idUnidad = id_unidad)
    if request.method == 'POST':
        UnidadOrganizacional.objects.filter(idUnidad = id_unidad).delete()
        unidad.delete()
        return redirect('index unidad')
    return render(request, 'unidad/delete_unidad.html', {'unidad':unidad})