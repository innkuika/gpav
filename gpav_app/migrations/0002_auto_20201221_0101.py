# Generated by Django 3.1.4 on 2020-12-21 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpav_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='avatar_url',
            field=models.URLField(null=True),
        ),
    ]