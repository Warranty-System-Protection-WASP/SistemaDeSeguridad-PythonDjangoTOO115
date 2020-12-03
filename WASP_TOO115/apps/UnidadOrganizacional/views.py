from django.shortcuts import render,redirect
from django.core import serializers
from django.http import HttpResponseRedirect
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

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
    success_url=reverse_lazy('UnidadOrganizacional:UnidadList') #Para que nos devuelva a la lista

    #
    def get_context_data(self, **kwargs):
        context=super(UnidadCreate, self).get_context_data(**kwargs)
        #Le mandamos el formulario en el context
        if 'form' is not context:
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





# # Create your views here.
# def index_unidad(request):
#     #Traemos todos los objetos
#     unidad=UnidadOrganizacional.objects.all()
#     context={'unidades':unidad}
#     #Retornamos a la vista
#     return render(request,'unidad/index_unidad.html',context)

# def view_unidad(request):
#     js_data=""
#     if request.method=='POST':
#         form=unidad_form(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('index unidad')
#     else:
#         form=unidad_form()    
#     return render(request, 'unidad/form_unidad.html',{'form':form, 'my_data':js_data})


# #Para editar la unidad necesitamos el id de la unidad
# def edit_unidad(request, id_unidad):
#     unidad=UnidadOrganizacional.objects.get(id= id_unidad)
#     acceso=UnidadOrganizacional.objects.filter(idUnidad=id_unidad)
#     js_data=serializers.serialize('json',acceso)
#     if request.method=='GET':
#         form=unidad_form(instance=rol)
#     else:
#         form=unidad_form(request.POST, instace=unidad)
#         if form.is_valid():
#             form.save()
#         return redirect('index unidad')
#     return request(request,'unidad/unidad_unidad.html',{'form':form, 'my_data':js_data})

# def delete_unidad(request, id_unidad):
#     return request('unidad/delete_unidad.html')


# def create_acceso(request):
#     if request.method == 'GET':
#         return render(request, 'unidad/acceso_unidad.html')

#     if request.method == 'POST':
#         if 'idunidad' in request.POST:
#             if 'estado' in request.POST:
#                 contador = 1
#                 for sw in switches:
#                     if request.POST['id'] == sw:
#                         try:
#                             obj = UnidadOrganizacional.objects.filter( idUnidad= 1, idOpcion = contador)
#                             if request.POST['estado'] == 'unchecked':
#                                 obj.delete()
#                             if request.POST['estado'] == 'checked':
#                                 with connection.cursor() as cursor:
#                                     #Query para insertar una nueva unidad organizacional
#                                     cursor.execute("INSERT INTO UNIDADORGANIZACIONAL_UNIDA4EEA (NOMBREUNIDAD,DESCRIPUNIDAD,IDROL_ID) VALUES ( %s, %s, %s );",[contador,1])
#                                     cursor.close()
#                         except:
#                             obj = UnidadOrganizacional.objects.filter(idRol = 1, idOpcion = contador)
#                             if request.POST['estado'] == 'unchecked':
#                                 obj.delete()
#                         return HttpResponse('success')
#                     contador +=1