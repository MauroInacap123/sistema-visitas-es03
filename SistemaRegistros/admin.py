"""
Configuración del panel de administración de Django
"""

from django.contrib import admin
from .models import Visita
import csv
from django.http import HttpResponse


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'rut', 'nombre', 'motivo_corto', 'fecha_entrada', 'hora_salida', 'estado']
    list_filter = ['fecha_entrada', 'hora_salida']
    search_fields = ['rut', 'nombre', 'motivo']
    readonly_fields = ['fecha_entrada']
    ordering = ['-fecha_entrada']
    list_per_page = 20
    
    def motivo_corto(self, obj):
        """Muestra solo los primeros 50 caracteres del motivo"""
        return obj.motivo[:50] + '...' if len(obj.motivo) > 50 else obj.motivo
    motivo_corto.short_description = 'Motivo'
    
    def estado(self, obj):
        """Muestra el estado de la visita"""
        return obj.estado
    estado.short_description = 'Estado'
    
    actions = ['marcar_salida_masivo', 'exportar_csv']
    
    def marcar_salida_masivo(self, request, queryset):
        """Acción para marcar la salida de múltiples visitas"""
        from django.utils import timezone
        
        actualizadas = 0
        for visita in queryset:
            if not visita.hora_salida:
                visita.hora_salida = timezone.now().time()
                visita.save()
                actualizadas += 1
        
        self.message_user(request, f'{actualizadas} visita(s) marcada(s) con salida')
    marcar_salida_masivo.short_description = 'Marcar salida masiva'
    
    def exportar_csv(self, request, queryset):
        """Acción para exportar visitas a CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="visitas.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'RUT', 'Nombre', 'Motivo', 'Fecha Entrada', 'Hora Salida', 'Estado'])
        
        for visita in queryset:
            writer.writerow([
                visita.id,
                visita.rut,
                visita.nombre,
                visita.motivo,
                visita.fecha_entrada,
                visita.hora_salida or 'No registrada',
                visita.estado
            ])
        
        return response
    exportar_csv.short_description = 'Exportar a CSV'


# Personalizar el admin site
admin.site.site_header = "Sistema de Registro de Visitas - Admin"
admin.site.site_title = "Admin Visitas"
admin.site.index_title = "Panel de Administración"
