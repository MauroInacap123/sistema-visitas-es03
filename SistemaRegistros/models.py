"""
Modelos de la aplicación SistemaRegistros - ES02/ES03
"""

from django.db import models
from django.core.exceptions import ValidationError
import re


def validar_rut(rut):
    """
    Valida formato de RUT chileno
    Formato aceptado: XX.XXX.XXX-X o XXXXXXXX-X
    """
    # Limpiar el RUT de puntos y guiones para validación
    rut_limpio = rut.replace('.', '').replace('-', '')
    
    if len(rut_limpio) < 2:
        raise ValidationError('RUT inválido: demasiado corto')
    
    # Validar que tenga formato correcto
    if not re.match(r'^\d{1,8}[\dkK]$', rut_limpio):
        raise ValidationError('RUT inválido: formato incorrecto. Use formato XX.XXX.XXX-X')
    
    # Extraer número y dígito verificador
    numero = rut_limpio[:-1]
    dv = rut_limpio[-1].upper()
    
    # Calcular dígito verificador
    suma = 0
    multiplo = 2
    
    for i in reversed(numero):
        suma += int(i) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    
    if dv != dv_calculado:
        raise ValidationError(f'RUT inválido: dígito verificador incorrecto')


class Visita(models.Model):
    """
    Modelo para registrar visitas
    """
    rut = models.CharField(
        max_length=12,
        validators=[validar_rut],
        verbose_name='RUT',
        help_text='Formato: XX.XXX.XXX-X'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre Completo'
    )
    motivo = models.TextField(
        verbose_name='Motivo de la Visita'
    )
    fecha_entrada = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y Hora de Entrada'
    )
    hora_salida = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Hora de Salida'
    )
    
    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-fecha_entrada']
    
    def __str__(self):
        return f"{self.nombre} - {self.rut}"
    
    @property
    def estado(self):
        """
        Retorna el estado de la visita
        """
        return 'Activo' if self.hora_salida is None else 'Completado'
