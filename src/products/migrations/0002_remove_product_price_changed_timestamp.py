# Generated by Django 4.1.8 on 2023-04-30 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_changed_timestamp',
        ),
    ]
