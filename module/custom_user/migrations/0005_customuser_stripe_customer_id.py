# Generated by Django 5.0.3 on 2024-04-09 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0004_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
