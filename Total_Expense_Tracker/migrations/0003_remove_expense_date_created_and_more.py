# Generated by Django 4.2.13 on 2024-06-12 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Total_Expense_Tracker', '0002_globalvariable_rename_expenses_expense'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='income',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='date_created',
        ),
    ]
