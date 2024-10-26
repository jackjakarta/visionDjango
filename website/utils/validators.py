import os

from django.core.exceptions import ValidationError


def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [
        ".mp4",
    ]

    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Only .mp4 is supported.")


def validate_video_size(value):
    max_size = 15 * 1024 * 1024  # 15MB in bytes

    if value.size > max_size:
        raise ValidationError("File too large. Size should not exceed 15MB.")
