# Generated by Django 4.2 on 2024-07-19 20:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0022_customer_username_alter_customer_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
