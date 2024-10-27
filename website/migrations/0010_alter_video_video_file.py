# Generated by Django 5.0.4 on 2024-04-19 10:27

from django.db import migrations, models

import website.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0009_alter_narration_audio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="video_file",
            field=models.FileField(
                upload_to="videos/",
                validators=[
                    website.utils.validators.validate_video_extension,
                    website.utils.validators.validate_video_size,
                ],
            ),
        ),
    ]
