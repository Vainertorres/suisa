# Generated by Django 4.0.4 on 2022-08-27 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cnf', '0002_etnia_codigo'),
        ('sam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establecimiento',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Dptoubica', to='cnf.departamento'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='dptonotifica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dptonotifica', to='cnf.departamento'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='mpionotifica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mpionotifica', to='cnf.municipio'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mpioubica', to='cnf.municipio'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='propietario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codpropietario', to='sam.propietario'),
        ),
        migrations.AlterField(
            model_name='establecimiento',
            name='replegal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codreplegal', to='sam.propietario'),
        ),
    ]