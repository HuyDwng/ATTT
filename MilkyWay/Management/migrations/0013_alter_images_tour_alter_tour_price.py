# Generated by Django 5.1.2 on 2024-10-31 10:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0012_payment_payment_state_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='tour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Management.tour'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
