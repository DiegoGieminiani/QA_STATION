# Generated by Django 5.1.1 on 2024-11-17 23:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('test_case_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID del Caso de Prueba')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre del Caso de Prueba')),
                ('url', models.URLField(max_length=2048, verbose_name='URL del Caso de Prueba')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('resultado_esperado', models.TextField(verbose_name='Resultado Esperado')),
                ('functional_test_id', models.IntegerField(verbose_name='ID de la Prueba Funcional Asociada')),
            ],
            options={
                'verbose_name': 'Caso de Prueba',
                'verbose_name_plural': 'Casos de Prueba',
            },
        ),
        migrations.CreateModel(
            name='StepByStep',
            fields=[
                ('id_paso', models.AutoField(primary_key=True, serialize=False, verbose_name='ID del Paso')),
                ('pasos', models.TextField(verbose_name='Descripción del Paso')),
                ('orden', models.PositiveIntegerField(verbose_name='Orden del Paso')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='ai_module.testcase', verbose_name='Caso de Prueba Asociado')),
            ],
            options={
                'verbose_name': 'Paso a Paso',
                'verbose_name_plural': 'Pasos a Paso',
            },
        ),
    ]
