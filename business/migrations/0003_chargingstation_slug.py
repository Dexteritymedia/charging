# Generated by Django 4.2 on 2024-04-29 23:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargingstation',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, null=True),
        ),
    ]