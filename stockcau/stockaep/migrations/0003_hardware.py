# Generated by Django 4.2.3 on 2023-07-24 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0002_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stockaep.tipo')),
            ],
        ),
    ]
