# Generated by Django 4.0.4 on 2023-06-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnf', '0004_barrio_lat_barrio_lon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='apellido1',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='apellido2',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nombre1',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nombre2',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
