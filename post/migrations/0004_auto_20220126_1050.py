# Generated by Django 3.1.14 on 2022-01-26 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20220126_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
