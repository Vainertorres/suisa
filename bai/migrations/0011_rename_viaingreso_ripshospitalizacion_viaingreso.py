# Generated by Django 4.0.4 on 2023-07-27 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bai', '0010_alter_ripsurgencia_options_ripshospitalizacion_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ripshospitalizacion',
            old_name='ViaIngreso',
            new_name='viaingreso',
        ),
    ]