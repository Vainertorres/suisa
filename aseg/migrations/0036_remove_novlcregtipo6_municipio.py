# Generated by Django 4.2.7 on 2024-01-18 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aseg', '0035_estadolc_novlcregtipo6'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novlcregtipo6',
            name='municipio',
        ),
    ]