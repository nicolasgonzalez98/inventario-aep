# Generated by Django 4.2.3 on 2023-08-29 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0018_contador_alter_notificacion_hardware'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='observaciones',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]
