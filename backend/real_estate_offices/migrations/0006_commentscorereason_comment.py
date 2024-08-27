# Generated by Django 5.0 on 2024-08-27 16:22

import common.utils.database
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate_offices', '0005_rename_instagram_realestateoffice_facebook_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentScoreReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=common.utils.database.formated_datetime_now)),
                ('modified_at', models.DateTimeField(default=common.utils.database.formated_datetime_now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_office_comment', to=settings.AUTH_USER_MODEL)),
                ('real_estate_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='real_estate_offices.realestateoffice')),
                ('score_reason', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='real_estate_offices.commentscorereason')),
            ],
        ),
    ]
