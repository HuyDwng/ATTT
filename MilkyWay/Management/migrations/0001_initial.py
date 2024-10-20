# Generated by Django 5.1.2 on 2024-10-21 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('booked', 'Booked'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='booked', max_length=10)),
                ('payment_method', models.CharField(blank=True, max_length=50)),
                ('ticket_code', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_code', models.IntegerField()),
                ('issued_date', models.DateTimeField()),
                ('ticket_status', models.CharField(choices=[('issued', 'Issued'), ('use', 'Used'), ('cancelled', 'Cancelled')], default='issued', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_location', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_seats', models.IntegerField()),
                ('images', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('fullname', models.CharField(max_length=200)),
                ('role', models.CharField(choices=[('customer', 'Customer'), ('staff', 'Staff'), ('admin', 'Admin')], default='customer', max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_joined', models.DateTimeField()),
                ('is_actived', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=50)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Management.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.tour'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField(blank=True)),
                ('review_date', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.users')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.users'),
        ),
    ]
