# Generated by Django 2.2.7 on 2019-12-07 22:02

import django.db.models.deletion
from django.db import migrations
from django.db import models

import pitter.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('pitter', '0002_auto_20191206_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                (
                    'id',
                    models.CharField(
                        default=pitter.models.base.default_uuid_id,
                        editable=False,
                        max_length=256,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('speech_audio_file', models.FileField(upload_to='')),
                ('speech_transcript', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pitter.User')),
            ],
            options={'abstract': False,},
        ),
    ]