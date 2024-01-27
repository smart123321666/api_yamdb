# Generated by Django 3.2 on 2024-01-27 11:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_merge_20240125_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='description',
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10, 'Оценка не может\n                                   быть больше %(limit_value)s.'), django.core.validators.MinValueValidator(0, 'Оценка не может\n                                  быть ниже %(limit_value)s.')], verbose_name='Оценка'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_title_author'),
        ),
    ]
