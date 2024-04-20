import base64

import cv2
from openai import OpenAI
from django.conf import settings


class VideoAnalyser:
    def __init__(self, video: str, custom_prompt: str = None):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.video = cv2.VideoCapture(video)
        self.base64frames = None
        self.generated_text = None
        self.custom_prompt = custom_prompt

    def _read_frames(self):
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

    def generate_narration(self):
        self._read_frames()

        if self.base64frames is None or not self.base64frames:
            print("No frames to generate narration from.")
            return None

        video_duration = len(self.base64frames) / 30
        prompt = [
            {
                "role": "system",
                "content": "You are an AI vision model that generates voice-overs based on a video input by analyzing "
                           "the frames. You follow instructions very strictly.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "These are frames of a video. Create a short voiceover script. Only include the "
                                f"narration in plain text. The video is {video_duration:.2f} seconds long. Follow "
                                "custom instructions carefully if there are any provided below.\n\n"
                                f"Custom Instructions:\n\n{self.custom_prompt}",
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{frame}",
                                "detail": "low",
                            }
                        } for frame in self.base64frames[0::50]
                    ],
                ]
            }
        ]

        debug_print = prompt[1].get("content")[0]
        print(f"\n**********PROMPT**********\n{debug_print}\n")

        params = {
            "model": "gpt-4-turbo",
            "messages": prompt,
            "max_tokens": 350,
            "temperature": 0.7,
            "frequency_penalty": 1,
            "presence_penalty": 1,
        }

        text_generation = self.client.chat.completions.create(**params)
        self.generated_text = text_generation.choices[0].message.content

        return self.generated_text
