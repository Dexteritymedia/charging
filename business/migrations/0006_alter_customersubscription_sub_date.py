# Generated by Django 4.2 on 2024-04-29 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_alter_chargingstation_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersubscription',
            name='sub_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
