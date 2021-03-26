# Generated by Django 3.1.4 on 2021-03-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpav_app', '0017_auto_20201225_0237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='media_data',
        ),
        migrations.RemoveField(
            model_name='pollchoice',
            name='choice_image',
        ),
        migrations.AddField(
            model_name='media',
            name='media_file',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='pollchoice',
            name='choice_image_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
