# Generated by Django 5.0 on 2024-10-05 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0018_alter_suggestedsearch_query'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suggestedsearch',
            old_name='display_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='suggestedsearch',
            name='query',
        ),
    ]
