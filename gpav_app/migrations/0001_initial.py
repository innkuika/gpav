# Generated by Django 3.1.4 on 2020-12-19 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
                ('content_html', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('name', models.CharField(max_length=256)),
                ('id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('avatar_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
                ('content_html', models.CharField(max_length=1024)),
                ('audience_html', models.CharField(max_length=1024)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='gpav_app.person')),
                ('comments', models.ManyToManyField(to='gpav_app.Comment')),
                ('plus_oners', models.ManyToManyField(related_name='plus_oners', to='gpav_app.Person')),
                ('resharers', models.ManyToManyField(related_name='resharers', to='gpav_app.Person')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gpav_app.person'),
        ),
    ]
