# Generated by Django 5.1.1 on 2024-10-24 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ai_module', '0001_initial'),
        ('user_projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionalTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.JSONField(verbose_name='JSON Data')),
                ('origin', models.CharField(max_length=255, verbose_name='Origin')),
                ('execution', models.CharField(max_length=255, verbose_name='Execution Status')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='functional_tests', to='user_projects.project', verbose_name='Project')),
                ('test_case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='functional_tests', to='ai_module.testcase', verbose_name='Test Case')),
            ],
            options={
                'verbose_name': 'Functional Test',
                'verbose_name_plural': 'Functional Tests',
                'ordering': ['execution'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=50, null=True, verbose_name='Result Status')),
                ('description', models.TextField(verbose_name='Result Description')),
                ('evidence', models.TextField(blank=True, null=True, verbose_name='Evidence')),
                ('test_results', models.JSONField(verbose_name='Test Results')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('functional_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='functional_tests.functionaltest', verbose_name='Functional Test')),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'Results',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='functionaltest',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='functional_tests.result', verbose_name='Result'),
        ),
    ]
