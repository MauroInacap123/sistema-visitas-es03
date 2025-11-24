"""
Vistas tradicionales de Django (templates)
Para mantener compatibilidad con ES02
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Visita


def lista_visitas(request):
    """
    Lista todas las visitas con paginación
    """
    visitas_list = Visita.objects.all().order_by('-fecha_entrada')
    paginator = Paginator(visitas_list, 10)  # 10 visitas por página
    
    page_number = request.GET.get('page')
    visitas = paginator.get_page(page_number)
    
    context = {
        'visitas': visitas,
        'total_visitas': visitas_list.count()
    }
    return render(request, 'SistemaRegistros/lista_visitas.html', context)


def registrar_visita(request):
    """
    Registra una nueva visita
    """
    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        motivo = request.POST.get('motivo')
        
        try:
            visita = Visita.objects.create(
                rut=rut,
                nombre=nombre,
                motivo=motivo
            )
            messages.success(request, 'Visita registrada exitosamente')
            return redirect('lista_visitas')
        except Exception as e:
            messages.error(request, f'Error al registrar la visita: {str(e)}')
    
    return render(request, 'SistemaRegistros/registrar_visita.html')


def editar_visita(request, pk):
    """
    Edita una visita existente
    """
    visita = get_object_or_404(Visita, pk=pk)
    
    if request.method == 'POST':
        visita.rut = request.POST.get('rut')
        visita.nombre = request.POST.get('nombre')
        visita.motivo = request.POST.get('motivo')
        hora_salida = request.POST.get('hora_salida')
        
        if hora_salida:
            visita.hora_salida = hora_salida
        
        try:
            visita.save()
            messages.success(request, 'Visita actualizada exitosamente')
            return redirect('lista_visitas')
        except Exception as e:
            messages.error(request, f'Error al actualizar la visita: {str(e)}')
    
    context = {'visita': visita}
    return render(request, 'SistemaRegistros/editar_visita.html', context)


def eliminar_visita(request, pk):
    """
    Elimina una visita
    """
    visita = get_object_or_404(Visita, pk=pk)
    
    if request.method == 'POST':
        try:
            visita.delete()
            messages.success(request, 'Visita eliminada exitosamente')
            return redirect('lista_visitas')
        except Exception as e:
            messages.error(request, f'Error al eliminar la visita: {str(e)}')
    
    context = {'visita': visita}
    return render(request, 'SistemaRegistros/eliminar_visita.html', context)
