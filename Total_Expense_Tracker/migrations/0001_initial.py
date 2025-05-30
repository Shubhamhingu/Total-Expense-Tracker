# Generated by Django 4.2.13 on 2024-06-11 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('is_cash', models.BooleanField(default=True)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('is_cash', models.BooleanField(default=True)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_worked', models.FloatField()),
                ('date_created', models.DateTimeField()),
                ('is_cash', models.BooleanField(default=True)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Total_Expense_Tracker.expenses')),
                ('tip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Total_Expense_Tracker.income')),
            ],
        ),
    ]
