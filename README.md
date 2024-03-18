# Video Narration Tool

## Introduction

This Django app leverages the power of GPT-4 Vision and OpenCV to analyze video frames, generating a context-aware narration based on these frames. The application opens new doors for content creators, educators, and anyone interested in automated video analysis and narration.

## Features

- **Video Frame Analysis:** Utilizes OpenCV to analyze each frame of the video and pass it to the OpenAI API
- **GPT-4 Vision:** Harnesses the advanced capabilities of GPT-4 Vision to interpret the analyzed frames, ensuring narrations are contextually relevant and insightful.
- **Custom Narration Styles:** Offers the flexibility to tailor the narration style to fit the video’s tone and audience, from formal documentaries to casual vlogs by giving custom instructions to the model.
- **Text-To-Speech:** Generates Text-To-Speech audio files from the narration text using OpenAI or ElevenLabs API.

## Requirements

Make sure you have `libgl1-mesa-glx` installed on you machine. This is needed for OpenCV:

```bash
sudo apt install libgl1-mesa-glx
```
