# Generated by Django 5.0 on 2024-08-06 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0004_rename_meterage_advertisement_area_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='floor_meterial',
            new_name='flooring',
        ),
        migrations.RenameField(
            model_name='advertisement',
            old_name='type',
            new_name='property_type',
        ),
        migrations.RenameField(
            model_name='advertisement',
            old_name='deal_type',
            new_name='type_of_transaction',
        ),
    ]