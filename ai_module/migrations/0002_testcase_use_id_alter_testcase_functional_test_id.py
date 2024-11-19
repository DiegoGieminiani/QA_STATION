# Generated by Django 5.1.1 on 2024-11-19 02:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_module', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='use_id',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testcase',
            name='functional_test_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ai_module.functionaltest'),
        ),
    ]
