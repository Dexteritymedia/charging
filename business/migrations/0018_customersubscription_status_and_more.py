# Generated by Django 4.2 on 2024-05-05 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0017_chargingstation_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customersubscription',
            name='status',
            field=models.CharField(blank=True, choices=[(0, 'Not charging'), (1, 'Charging'), (2, 'Charged')], default=0, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='chargingactivity',
            name='subscriber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='business.customer'),
        ),
    ]
