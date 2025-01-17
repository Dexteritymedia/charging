# Generated by Django 4.2 on 2024-04-29 23:26

import business.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_customersubscription_sub_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargingstation',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='customersubscription',
            name='sub_code',
            field=models.CharField(blank=True, default=business.models.generate_verification_code, max_length=300, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customersubscription',
            name='sub_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
