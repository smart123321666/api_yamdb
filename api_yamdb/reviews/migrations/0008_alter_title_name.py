# Generated by Django 3.2 on 2023-12-26 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_title_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=256, validators=[django.core.validators.MaxLengthValidator(256)], verbose_name='Наименование произведения'),
        ),
    ]