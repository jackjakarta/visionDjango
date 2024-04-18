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

        prompt = [
            {
                "role": "system",
                "content": "You are an AI vision model that generates narrations based on a video input by analysing "
                           "each frame.",
            },
            {
                "role": "user",
                "content": [
                    "These are frames from a video. Create a voice-over narration for this video. "
                    "The narration should be engaging and tailored to the video content. Please only give me the "
                    "narration in plain text without any other instructions.\n\nHere's how to proceed:\n\n"
                    
                    "1. Align the narration with any specific instructions or themes provided to enhance the "
                    "video's message.\n\n"
                    "2. Without specific directions, create a compelling narrative that complements the visual "
                    "flow and mood of the video.\n\n"
                    
                    f"The video has {len(self.base64frames)} frames at 30 fps. Adjust the output length to fit when "
                    "spoken slowly and then and make it half the length. Please strictly adhere to this "
                    "instruction. \n\n"
                    
                    "Here are the customisation details if any available:\n\n"
                    f"{self.custom_prompt}\n",
                    *map(lambda x: {"image": x, "resize": 768}, self.base64frames[0::50]),
                ],
            }
        ]
        print(f"\n**********PROMPT**********\n{prompt}\n")

        params = {
            "model": "gpt-4-vision-preview",
            "messages": prompt,
            "max_tokens": 256,
            "temperature": 0.6,
            "frequency_penalty": 0.7,
            "presence_penalty": 0.7,
        }

        text_generation = self.client.chat.completions.create(**params)
        self.generated_text = text_generation.choices[0].message.content

        return self.generated_text
