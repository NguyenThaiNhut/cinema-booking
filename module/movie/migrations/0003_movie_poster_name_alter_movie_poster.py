# Generated by Django 5.0.3 on 2024-05-03 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_movie_trailer'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.TextField(blank=True, null=True),
        ),
    ]