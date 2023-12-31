# Generated by Django 4.2.4 on 2023-11-02 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=50)),
                ('client_phone', models.CharField(max_length=15)),
                ('client_address', models.CharField(blank=True, max_length=100)),
                ('client_contact', models.CharField(max_length=50)),
                ('client_email', models.EmailField(max_length=254)),
                ('client_account_number', models.CharField(max_length=20)),
                ('rate', models.CharField(default='0', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.IntegerField()),
                ('invoice_date', models.DateField()),
                ('due_date', models.DateField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.client')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_work', models.DateField()),
                ('description', models.CharField(max_length=100)),
                ('hours', models.CharField(max_length=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice')),
            ],
        ),
    ]
