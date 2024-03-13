import requests
from openai import OpenAI
from django.conf import settings


class OpenTTS:
    """Text-To-Speech using ElevenLabs API."""
    def __init__(self, text, voice="fable", model="tts-1"):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.voice = voice
        self.model = model
        self.text = text
        self.response = None

    def generate(self):
        self.response = self.client.audio.speech.create(
            input=self.text,
            model=self.model,
            voice=self.voice,  # NOQA
        )

        return self.response.iter_bytes(1024)


class ElevenLabsTTS:
    """Text-To-Speech using ElevenLabs API."""
    def __init__(self, text, voice, model="eleven_multilingual_v2"):
        self.text = text
        self.voice = voice
        self.model = model
        self.response = None

    def generate(self):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY
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

        return self.response.content
