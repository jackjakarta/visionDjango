from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from website.audio.tts import OpenTTS
from website.models import Narration
from .serializers import NarrationSerializer, TTSSerializer


class NarrationsViewSet(viewsets.ModelViewSet):
    queryset = Narration.objects.all()
    serializer_class = NarrationSerializer
    parser_classes = (MultiPartParser, FormParser, )

    def get_queryset(self):
        if not isinstance(self.request.user, AnonymousUser):
            user_id = self.request.user.id

            return Narration.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_success_headers(self, data):
        try:
            return {'Location': "Yes Yes"}
        except (TypeError, KeyError):
            return {}


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tts_create(request):
    text = request.data.get("text")
    voice = request.data.get("voice")
    quality = request.data.get("quality")

    if not text:
        return Response(
            data={"error": "Please provide 'text' argument in the request."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if voice not in ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'] and voice is not None:
        return Response(
            data={
                "error": "Voice doesn't exist. Please choose from following voices: 'alloy', 'echo', 'fable', 'onyx', "
                         "'nova', 'shimmer'",
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if quality not in ["standard", "hd"] and quality is not None:
        return Response(
            data={"error": "Wrong 'quality' parameter. Please choose between 'fast' and 'hd'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = TTSSerializer(
        data={
            'text': text,
            'voice': voice if voice else "fable",
            'quality': quality if quality else "standard",
        }
    )

    if serializer.is_valid():
        validated_text = serializer.validated_data.get("text")
        validated_voice = serializer.validated_data.get("voice")
        validated_quality = serializer.validated_data.get("quality")

        tts = OpenTTS(
            text=validated_text,
            voice=validated_voice,
            model="tts-1-hd" if validated_quality == "hd" else "tts-1"
        )
        audio_obj = tts.speech_for_api()

        return Response(
            data={
                "voice": validated_voice,
                "quality": validated_quality,
                "text": validated_text,
                "file": audio_obj.audio_file.url,
            },
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
