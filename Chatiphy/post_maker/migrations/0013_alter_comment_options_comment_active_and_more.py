# Generated by Django 5.1.1 on 2024-10-19 20:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_maker', '0012_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created'], name='post_maker__created_a73185_idx'),
        ),
    ]