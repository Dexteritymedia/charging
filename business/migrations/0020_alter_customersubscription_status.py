# Generated by Django 4.2 on 2024-05-05 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0019_alter_customersubscription_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersubscription',
            name='status',
            field=models.CharField(blank=True, choices=[(0, 'Not charging'), (1, 'Charging'), (2, 'Charged')], default=0, max_length=10, null=True),
        ),
    ]