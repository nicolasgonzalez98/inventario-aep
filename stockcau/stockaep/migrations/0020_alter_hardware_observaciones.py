# Generated by Django 4.2.3 on 2023-08-29 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0019_alter_hardware_observaciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hardware',
            name='observaciones',
            field=models.TextField(default='', max_length=500),
        ),
    ]