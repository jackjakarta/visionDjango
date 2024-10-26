from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "video_file"]
        widgets = {"title": forms.TextInput(attrs={"placeholder": "My first project"})}
        labels = {
            "title": "Project Name",
        }
        help_texts = {
            "title": "Give your project a title in order to find it later.",
            "video_file": "<b>15MB</b> max. Supported formats: <b>.mp4</b> only",
        }
