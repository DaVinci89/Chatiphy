# Generated by Django 5.1.1 on 2024-09-27 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_maker', '0008_alter_post_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
