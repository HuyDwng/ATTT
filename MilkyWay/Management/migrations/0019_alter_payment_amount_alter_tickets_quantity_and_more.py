# Generated by Django 5.1.2 on 2024-11-05 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0018_alter_booking_status_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='quantity',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='ticket_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tour',
            name='available_seats',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='tour',
            name='price',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='tour',
            name='remaining_seats',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]