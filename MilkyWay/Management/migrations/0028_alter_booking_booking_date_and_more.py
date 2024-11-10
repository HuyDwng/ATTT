# Generated by Django 5.1.2 on 2024-11-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0027_alter_payment_booking_alter_tickets_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('transfer', 'Transfer'), ('cash', 'Cash'), ('credit-card', 'Credit-card'), ('e-wallet', 'E-wallet')], default='transfer', max_length=15),
        ),
    ]
