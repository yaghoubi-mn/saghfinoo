# Generated by Django 5.0 on 2024-09-04 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpage',
            name='content',
            field=models.TextField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='mainpage',
            name='page',
            field=models.CharField(max_length=50),
        ),
    ]
