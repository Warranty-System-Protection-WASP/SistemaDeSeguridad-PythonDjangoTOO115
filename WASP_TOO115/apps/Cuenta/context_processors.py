from .models import Departamento, Municipio

def ContextoGlobal(request):
    departamento = Departamento.objects.all()
    municipio = Municipio.objects.all()
    return {'departamento':departamento, 'municipio':municipio}
