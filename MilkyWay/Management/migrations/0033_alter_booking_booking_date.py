# Generated by Django 5.1.2 on 2024-11-11 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0032_merge_20241111_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(),
        ),
    ]