# Generated by Django 5.0.3 on 2024-04-15 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SeatDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_row', models.IntegerField()),
                ('seats_column', models.IntegerField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall.hall')),
                ('seat_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hall.seattype')),
            ],
        ),
    ]
