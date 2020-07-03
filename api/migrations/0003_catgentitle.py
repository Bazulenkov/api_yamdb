# Generated by Django 3.0.5 on 2020-07-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_catgentitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genres',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='api.GenreTitle', to='api.Genre'),
        ),
    ]