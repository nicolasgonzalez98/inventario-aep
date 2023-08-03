# Generated by Django 4.2.3 on 2023-07-24 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0007_alter_marca_nombre_alter_tipo_name_modelo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='hardware',
            name='estado',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='hardware',
            name='nro_de_serie',
            field=models.CharField(default='S/D', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='hardware',
            name='observaciones',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='hardware',
            name='ubicacion',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='stockaep.ubicacion'),
        ),
    ]