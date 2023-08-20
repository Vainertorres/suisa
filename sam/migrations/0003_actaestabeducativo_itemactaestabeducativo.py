# Generated by Django 4.0.4 on 2022-08-27 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cnf', '0002_etnia_codigo'),
        ('sam', '0002_alter_establecimiento_departamento_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActaEstabEducativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateField()),
                ('nroacta', models.CharField(max_length=15)),
                ('ciudad', models.CharField(max_length=30)),
                ('nombrerector', models.CharField(blank=True, max_length=100, null=True)),
                ('identificacionrector', models.CharField(blank=True, max_length=20, null=True)),
                ('nroestjormanhombres', models.IntegerField(default=0)),
                ('nroestjormanmujeres', models.IntegerField(default=0)),
                ('nroestjortarhombres', models.IntegerField(default=0)),
                ('nroestjortarmujeres', models.IntegerField(default=0)),
                ('nroestjornochombres', models.IntegerField(default=0)),
                ('nroestjornocmujeres', models.IntegerField(default=0)),
                ('nrodocenteshombres', models.IntegerField(default=1)),
                ('nrodocentesmujeres', models.IntegerField(default=1)),
                ('nroaulas', models.IntegerField(default=1)),
                ('nropatios', models.IntegerField(default=0)),
                ('nrocafeterias', models.IntegerField(default=0)),
                ('fechaultinspeccion', models.DateField(blank=True, null=True)),
                ('nroactaultinspeccion', models.CharField(blank=True, max_length=15, null=True)),
                ('concepto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Concepto', to='sam.concepto')),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sam.establecimiento')),
                ('motivoVisita', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sam.motivovisita')),
                ('tipodocrector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipodocrector', to='cnf.tipodoc')),
                ('uc', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario automatio')),
                ('ultconcepto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ultconcepto', to='sam.concepto')),
                ('um', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modifica')),
            ],
            options={
                'verbose_name': 'Acta de visita a establecimiento educativo',
            },
        ),
        migrations.CreateModel(
            name='ItemActaEstabEducativo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('hallazgos', models.TextField(blank=True, null=True)),
                ('puntaje', models.FloatField(default=0)),
                ('actaestabeducativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sam.actaestabeducativo')),
                ('evaluacion', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='sam.evaluacion')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sam.pregunta')),
                ('uc', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario automatio')),
                ('um', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modifica')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]