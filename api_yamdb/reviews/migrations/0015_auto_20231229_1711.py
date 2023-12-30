# Generated by Django 3.2 on 2023-12-29 17:11

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20231229_1708'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, title=django.db.models.expressions.F('author')), name='prevent_self_follow'),
        ),
    ]
