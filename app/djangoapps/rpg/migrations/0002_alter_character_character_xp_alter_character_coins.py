# Generated by Django 4.1.8 on 2023-05-03 21:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rpg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='character_xp',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator]),
        ),
        migrations.AlterField(
            model_name='character',
            name='coins',
            field=models.IntegerField(default=0),
        ),
    ]
