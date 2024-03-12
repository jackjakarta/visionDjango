import base64
import os

import cv2
from decouple import config
from openai import OpenAI

from website.utils import RandomGenerator

OPENAI_API_KEY = config("OPENAI_API_KEY")


class VideoAnalyser:
    def __init__(self, video: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.video = cv2.VideoCapture(video)
        self.base64frames = None
        self.generated_text = None

    def read_frames(self):
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
        if self.base64frames is None or not self.base64frames:
            print("No frames to generate narration from.")
            return None

        prompt = [
            {
                "role": "user",
                "content": [
                    "These are frames from a video. Generate a short but compelling narration that I can use as a "
                    "voice-over along with the video. Please only give me the narration in plain text without any "
                    "other instructions. Make sure that the text you generate fits and does not exceed the length of "
                    f"the video when spoken at a slow pace. The video is {len(self.base64frames)} frames long playing "
                    "at 30 fps.\n",
                    *map(lambda x: {"image": x, "resize": 768}, self.base64frames[0::50]),
                ],
            },
        ]
        print(f"\n**********PROMPT**********\n{prompt[0].get('content')[0]}\n")

        params = {
            "model": "gpt-4-vision-preview",
            "messages": prompt,
            "max_tokens": 800,
        }

        text_generation = self.client.chat.completions.create(**params)
        self.generated_text = text_generation.choices[0].message.content

        return self.generated_text

    def generate_speech(self):
        random_string = RandomGenerator(6).random_digits()
        audio_folder = "audio"
        os.makedirs(audio_folder, exist_ok=True)
        audio_path = os.path.join(audio_folder, f"speech_{random_string}.wav")

        audio_response = self.client.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=str(self.generated_text),
        )

        audio_response.stream_to_file(audio_path)
        print(f"Audio saved at {audio_path}.\n")
