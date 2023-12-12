# Generated by Django 3.2 on 2023-12-12 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='title', to='api.title'),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(to='api.Genre'),
        ),
    ]