from django.contrib.auth import get_user_model
from rest_framework import serializers

from website.models import Narration, Video, Audio

AuthUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['email']


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        exclude = []


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = []


class NarrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all(), required=False)
    audio = AudioSerializer()
    video = VideoSerializer()

    class Meta:
        model = Narration
        exclude = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user

        if user:
            representation['user'] = UserSerializer(user).data

        return representation


class TTSSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=250, required=True)
    voice = serializers.CharField(max_length=10, required=True)
    quality = serializers.CharField(max_length=10, required=True)
