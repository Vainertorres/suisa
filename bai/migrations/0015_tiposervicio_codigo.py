# Generated by Django 4.0.4 on 2023-07-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bai', '0014_ripsotrosservicios'),
    ]

    operations = [
        migrations.AddField(
            model_name='tiposervicio',
            name='codigo',
            field=models.CharField(default=1, max_length=1, unique=True),
            preserve_default=False,
        ),
    ]
