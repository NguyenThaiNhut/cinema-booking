# Generated by Django 5.0.3 on 2024-05-02 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0009_customuser_stripe_pm_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
