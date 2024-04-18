import base64

import cv2
from openai import OpenAI
from django.conf import settings


def calculate_video_duration(frames: int, fps: int) -> float:
    duration_seconds = frames / fps
    return duration_seconds


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
                "content": "You are an AI vision model that generates narrations based on a video input by analysing "
                           "each frame. You follow instructions very carefully.",
            },
            {
                "role": "user",
                "content": [
                    "These are frames from a video. Create a voice-over narration for this video. "
                    "The narration should be engaging and tailored to the video content. Please only give me the "
                    "narration in plain text without any other instructions.\n\nHere's how to proceed:\n\n"
                    
                    "1. Align the narration with any specific instructions or themes provided to enhance the "
                    "video's message but don't use very pretentious words unless instructed.\n"
                    "2. Without specific directions, create a compelling but short narrative that complements the "
                    "visual flow and mood of the video.\n\n"
                    
                    f"The video is {video_duration:.2f} seconds long. Adjust the narration length to fit the video "
                    "exactly when spoken at a slower pace. Please strictly follow this instruction. \n\n"
                    
                    f"Below are the customisation details if any available.\n\n{self.custom_prompt}\n",

                    # Frames from video
                    *map(lambda x: {"image": x, "resize": 768}, self.base64frames[0::50]),
                ],
            }
        ]
        print(f"\n**********PROMPT**********\n{prompt[1].get('content')[0]}\n")

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
