# Generated by Django 4.0.4 on 2023-06-24 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cnf', '0005_alter_paciente_apellido1_alter_paciente_apellido2_and_more'),
        ('bai', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ripsconsulta',
            options={'ordering': ['fechacons', 'paciente'], 'verbose_name_plural': 'Rips de consulta'},
        ),
        migrations.AlterModelOptions(
            name='ripsusuarios',
            options={'ordering': ['razonsocial'], 'verbose_name': 'Rips de Usuarios'},
        ),
        migrations.RenameField(
            model_name='ripsusuarios',
            old_name='primerapellido',
            new_name='apellido1',
        ),
        migrations.RenameField(
            model_name='ripsusuarios',
            old_name='segundoapellido',
            new_name='apellido2',
        ),
        migrations.RenameField(
            model_name='ripsusuarios',
            old_name='primernombre',
            new_name='nombre1',
        ),
        migrations.RenameField(
            model_name='ripsusuarios',
            old_name='segundonombre',
            new_name='nombre2',
        ),
        migrations.RemoveField(
            model_name='ripsconsulta',
            name='ripsUsuarios',
        ),
        migrations.RemoveField(
            model_name='ripsusuarios',
            name='regimen',
        ),
        migrations.AddField(
            model_name='ripsconsulta',
            name='paciente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cnf.paciente'),
        ),
        migrations.AddField(
            model_name='ripsconsulta',
            name='ripscontrol',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='bai.ripscontrol'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ripsusuarios',
            name='razonsocial',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='Tipousuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('codigo', models.IntegerField()),
                ('descripcion', models.CharField(max_length=100)),
                ('regimen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cnf.regimen')),
                ('uc', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario automatio')),
                ('um', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Modifica')),
            ],
            options={
                'verbose_name': 'Tipo de usuario',
                'ordering': ['descripcion'],
            },
        ),
        migrations.AddField(
            model_name='ripsusuarios',
            name='tipousuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bai.tipousuario'),
        ),
    ]
