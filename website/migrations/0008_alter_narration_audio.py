# Generated by Django 5.0.4 on 2024-04-16 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_audio_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='narration',
            name='audio',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audios', related_query_name='audio', to='website.audio'),
        ),
    ]
