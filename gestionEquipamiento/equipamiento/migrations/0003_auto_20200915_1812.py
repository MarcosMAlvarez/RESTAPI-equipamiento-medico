# Generated by Django 3.1.1 on 2020-09-15 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipamiento', '0002_auto_20200915_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distribuidor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=50)),
                ('tfno', models.IntegerField()),
                ('direccion', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'ordering': ['razon_social'],
            },
        ),
        migrations.AlterField(
            model_name='equipo',
            name='fecha_mantenimiento_anual',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='equipo',
            name='distribuidor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='distribuidor', to='equipamiento.distribuidor'),
            preserve_default=False,
        ),
    ]