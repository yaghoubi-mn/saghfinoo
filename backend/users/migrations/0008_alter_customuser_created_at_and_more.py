# Generated by Django 5.0 on 2024-06-30 06:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 6, 47, 44, 439999, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 6, 47, 44, 440021, tzinfo=datetime.timezone.utc)),
        ),
    ]