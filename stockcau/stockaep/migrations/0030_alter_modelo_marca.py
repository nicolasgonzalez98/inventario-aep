# Generated by Django 4.0.2 on 2023-09-18 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockaep', '0029_alter_estado_options_alter_modelo_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelo',
            name='marca',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='stockaep.marca'),
        ),
    ]
