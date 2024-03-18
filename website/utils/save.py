from secrets import token_urlsafe

from django.core.files.base import ContentFile

from website.models import Audio, Narration


def save_speech_to_db(narration: Narration, speech_content: bytes) -> Audio:
    if narration.text:
        file_name = f"speech_{narration.video.title}_{token_urlsafe(8)}.mp3"

        # Create a new Audio instance
        new_speech = Audio.objects.create(
            title=f"ID: {token_urlsafe(8)}",
        )

        # Create a Django File object from API response content
        django_file = ContentFile(speech_content, name=file_name)

        # Save to model field
        new_speech.audio_file.save(
            django_file.name,
            django_file,
            save=True
        )

        return new_speech
