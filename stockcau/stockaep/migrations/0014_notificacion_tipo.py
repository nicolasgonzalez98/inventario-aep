# Generated by Django 4.0.2 on 2023-08-24 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0013_notificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='tipo',
            field=models.CharField(default='POST', max_length=20),
            preserve_default=False,
        ),
    ]
