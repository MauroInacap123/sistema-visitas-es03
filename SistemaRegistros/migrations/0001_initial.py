# Generated migration

from django.db import migrations, models
import SistemaRegistros.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(help_text='Formato: XX.XXX.XXX-X', max_length=12, validators=[SistemaRegistros.models.validar_rut], verbose_name='RUT')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Completo')),
                ('motivo', models.TextField(verbose_name='Motivo de la Visita')),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Entrada')),
                ('hora_salida', models.TimeField(blank=True, null=True, verbose_name='Hora de Salida')),
            ],
            options={
                'verbose_name': 'Visita',
                'verbose_name_plural': 'Visitas',
                'ordering': ['-fecha_entrada'],
            },
        ),
    ]
