# Generated by Django 5.1.1 on 2024-09-26 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_maker', '0004_group_description_group_slug_group_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
