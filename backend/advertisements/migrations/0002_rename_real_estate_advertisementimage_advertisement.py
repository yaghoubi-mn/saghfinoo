# Generated by Django 5.0 on 2024-08-06 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisementimage',
            old_name='real_estate',
            new_name='advertisement',
        ),
    ]
