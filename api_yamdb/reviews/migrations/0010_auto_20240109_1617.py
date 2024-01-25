# Generated by Django 3.2 on 2024-01-09 16:17

import django.core.validators
import reviews.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['slug'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['pub_date'], 'verbose_name': 'Коментарий', 'verbose_name_plural': 'Коментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['slug'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['pub_date'], 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Текст коментария'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Наименование жанра'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10, 'Оценка не может быть больше %(limit_value)s.'), django.core.validators.MinValueValidator(0, 'Оценка не может быть ниже %(limit_value)s.')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст ревью'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.models.validate_year], verbose_name='Год'),
        ),
    ]
