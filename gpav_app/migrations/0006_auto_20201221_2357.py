# Generated by Django 3.1.4 on 2020-12-21 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpav_app', '0005_auto_20201221_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content_html',
            field=models.CharField(max_length=8192),
        ),
        migrations.AlterField(
            model_name='post',
            name='audience_html',
            field=models.CharField(max_length=8192),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_html',
            field=models.CharField(max_length=8192),
        ),
    ]
