# Generated by Django 4.0.2 on 2023-09-12 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0025_asignacion_nota_asignacion_nro_ticket_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacion',
            name='hardware',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='stockaep.hardware'),
        ),
    ]