# Generated by Django 3.2.9 on 2021-11-28 04:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reducer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urls',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]