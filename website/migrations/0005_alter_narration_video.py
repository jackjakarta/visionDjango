# Generated by Django 5.0.3 on 2024-03-18 03:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_video_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='narration',
            name='video',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='videos', related_query_name='video', to='website.video'),
        ),
    ]
