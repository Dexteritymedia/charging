# Generated by Django 4.2 on 2024-05-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_chargingstation_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingMonitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_code', models.CharField(blank=True, max_length=300, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('device', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
