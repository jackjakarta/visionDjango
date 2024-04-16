from secrets import token_urlsafe

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from openai import OpenAI

from website.models import Audio, Narration


class OpenTTS:
    """Text-To-Speech using OpenAI API."""
    def __init__(self, text, voice="fable", model="tts-1"):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.voice = voice
        self.model = model
        self.text = text
        self.response = None
        self.audio_data = b""
        self.byte_count = 0

    def __str__(self):
        audio_str = {
            "voice_id": self.voice,
            "model": self.model,
            "input_text": self.text,
        }

        return audio_str

    def _generate(self) -> bytes:
        self.response = self.client.audio.speech.create(
            input=self.text,
            model=self.model,
            voice=self.voice,  # NOQA
        )

        for chunk in self.response.iter_bytes(1024):
            self.audio_data += chunk

        self.byte_count = len(self.audio_data)

        return self.audio_data

    def speech_for_narration(self, narration: Narration) -> Audio:
        """
        Generates and saves TTS to narration in db.

        :return: Returns None and aborts save to db if input text is None or the file size is too low.
        """

        if narration.text:
            audio_data = self._generate()
            file_id = token_urlsafe(8)

            if self.byte_count > 220:
                file_name = f"speech_{narration.video.title}_{file_id}.mp3"

                # Create a new Audio instance
                new_speech = Audio.objects.create(
                    title=f"ID: {token_urlsafe(8)}",
                )

                # Create a Django File object from API response content
                django_file = ContentFile(audio_data, name=file_name)

                # Save to model field
                new_speech.audio_file.save(
                    django_file.name,
                    django_file,
                    save=True
                )

                return new_speech

    def speech_for_api(self) -> Audio:
        audio_data = self._generate()
        file_id = token_urlsafe(8)

        # Returns None if file size is under a certain size
        if self.byte_count > 220:
            file_name = f"speech_api_{file_id}.mp3"

            # Create a new Audio instance
            new_speech = Audio.objects.create(
                title=f"ID: {file_id}",
            )

            # Create a Django File object from API response content
            django_file = ContentFile(audio_data, name=file_name)

            # Save to model field
            new_speech.audio_file.save(
                django_file.name,
                django_file,
                save=True
            )

            return new_speech


class ElevenLabsTTS:
    """Text-To-Speech using ElevenLabs API."""
    def __init__(self, text, voice, model="eleven_turbo_v2"):
        self.text = text
        self.voice = voice
        self.model = model
        self.api_key = settings.ELEVENLABS_API_KEY
        self.response = None
        self.byte_count = 0

    def __str__(self):
        audio_str = {
            "voice_id": self.voice,
            "model": self.model,
            "input_text": self.text,
        }

        return audio_str

    def _generate(self) -> bytes:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        data = {
            "text": self.text,
            "model_id": self.model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        self.response = requests.post(url, json=data, headers=headers)
        self.byte_count = len(self.response.content)

        print(self.byte_count)  # DEBUG PRINT
        print(self.response.status_code)  # DEBUG PRINT
        return self.response.content

    def speech_for_narration(self, narration: Narration) -> Audio:
        """
        Generates and saves TTS to narration in db.

        :return: Returns None if input text is None or the file size is too low.
        """

        if narration.text:
            audio_data = self._generate()
            file_id = token_urlsafe(8)

            # Returns None if file size is a certain size
            if self.byte_count > 220:
                file_name = f"speech_{narration.video.title}_{file_id}.mp3"

                # Create a new Audio instance
                new_speech = Audio.objects.create(
                    title=f"ID: {file_id}",
                )

                # Create a Django File object from API response content
                django_file = ContentFile(audio_data, name=file_name)

                # Save to model field
                new_speech.audio_file.save(
                    django_file.name,
                    django_file,
                    save=True
                )

                return new_speech

    def speech_for_api(self, text: str) -> Audio:
        if text:
            audio_data = self._generate()
            file_id = token_urlsafe(8)

            # Returns None if file size is a certain size
            if self.byte_count > 220:
                file_name = f"speech_api_{file_id}.mp3"

                # Create a new Audio instance
                new_speech = Audio.objects.create(
                    title=f"ID: {file_id}",
                )

                # Create a Django File object from API response content
                django_file = ContentFile(audio_data, name=file_name)

                # Save to model field
                new_speech.audio_file.save(
                    django_file.name,
                    django_file,
                    save=True
                )

                return new_speech
