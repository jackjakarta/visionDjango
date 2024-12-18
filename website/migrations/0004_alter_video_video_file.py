# Generated by Django 5.0.3 on 2024-03-17 00:13

from django.db import migrations, models

import website.utils


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_alter_narration_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="video_file",
            field=models.FileField(
                upload_to="videos/", validators=[website.utils.validate_video_extension]
            ),
        ),
    ]
