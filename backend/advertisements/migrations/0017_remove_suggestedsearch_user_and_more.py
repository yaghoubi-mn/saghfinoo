# Generated by Django 5.0 on 2024-09-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0016_suggestedsearch_delete_clientsearch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestedsearch',
            name='user',
        ),
        migrations.AddField(
            model_name='suggestedsearch',
            name='display_name',
            field=models.CharField(default='d', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='suggestedsearch',
            name='query',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
