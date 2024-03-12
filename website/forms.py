from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Give your image a title in order to find it later..."
            })
        }
