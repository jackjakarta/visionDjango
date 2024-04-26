import base64

import cv2
from decouple import config
from django.conf import settings
from openai import OpenAI

from .constants import EXAMPLE_VOICEOVER


class VideoAnalyser:
    def __init__(self, video: str, custom_prompt: str | None = None) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.video = cv2.VideoCapture(video)
        self.base64frames = None
        self.generated_text = None
        self.custom_prompt = custom_prompt

    def _read_frames(self) -> list:
        if not self.video.isOpened():
            print("Error: Couldn't open video file.")
            return None

        self.base64frames = []
        while True:
            success, frame = self.video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            self.base64frames.append(base64.b64encode(buffer).decode("utf-8"))

        self.video.release()
        print(f"{len(self.base64frames)} frames read.")

        return self.base64frames

    def generate_narration(self) -> str:
        self._read_frames()

        if not self.base64frames:
            print("No frames to generate narration from.")
            return None

        video_duration = len(self.base64frames) / 30
        prompt = [
            {
                "role": "system",
                "content": "You are an AI vision model that generates voice-overs based by analyzing the frames of the video which are "
                           "provided to you as images. You follow instructions very strictly.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "As a professional scriptwriter, you are tasked with creating a compelling voiceover script for a video. "
                                "Follow these steps:\n\n1. You are to analyse the video frames provided.\n2. Create the voiceover based "
                                "on the content and length of the video.\n\nPlease only give me the voiceover in plain text without any "
                                f"other instructions. The video runs for {video_duration:.2f} seconds. The desired tone for the voiceover "
                                "should be casual, like one used in a youtube video unless instructed otherwise. Please refer to the provided "
                                f"custom instructions for additional guidance. Custom Instructions: {self.custom_prompt}\n\nExample "
                                f"Voiceover Script:\n\n{EXAMPLE_VOICEOVER}\n",
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{frame}",
                                "detail": config("VISION_DETAIL", default="low"),
                            }
                        } for frame in self.base64frames[0::50]
                    ],
                ]
            }
        ]

        debug_print = prompt[1].get("content")[0]
        print(f"\n**********PROMPT**********\n{debug_print}\n")

        params = {
            "messages": prompt,
            "model": config("VISION_MODEL", default="gpt-4-turbo"),
            "max_tokens": config("MODEL_MAX_TOKENS", default=1024, cast=int),
            "temperature": config("MODEL_TEMPERATURE", default=0.8, cast=float),
            "frequency_penalty": config("MODEL_FREQUENCY_PENALTY", default=0.4, cast=float),
            "presence_penalty": config("MODEL_PRESENCE_PENALTY", default=0.4, cast=float),
            "top_p": config("MODEL_TOP_P", default=1, cast=float),
        }

        text_generation = self.client.chat.completions.create(**params)
        self.generated_text = text_generation.choices[0].message.content

        return self.generated_text
