# Generated by Django 5.1.1 on 2024-11-09 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai_module", "0002_remove_document_document_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="testcase",
            name="a",
            field=models.IntegerField(default=0),
        ),
    ]
