# Generated by Django 5.1.2 on 2024-11-12 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0033_alter_booking_booking_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickets',
            name='issued_date',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_actived',
        ),
    ]