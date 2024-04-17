from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.viewsets import ReadOnlyModelViewSet

from website.audio.tts import OpenTTS
from website.models import Narration
from .serializers import NarrationSerializer, TTSSerializer


class NarrationViewSet(ReadOnlyModelViewSet):
    serializer_class = NarrationSerializer

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Response(data={"error": "403 - Forbidden."}, status=HTTP_403_FORBIDDEN)
        else:
            return Narration.objects.filter(user_id=self.request.user.id)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tts_create(request):
    text = request.data.get("text")
    voice = request.data.get("voice")
    quality = request.data.get("quality")

    if not text:
        return Response(data={"error": "Please provide 'text' argument in the request."}, status=HTTP_400_BAD_REQUEST)

    if voice not in ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'] and voice is not None:
        return Response(
            data={
                "error": "Voice doesn't exist. Please choose from following voices: 'alloy', 'echo', 'fable', 'onyx', "
                         "'nova', 'shimmer'",
            },
            status=HTTP_400_BAD_REQUEST
        )

    if quality not in ["standard", "hd"] and quality is not None:
        return Response(
            data={"error": "Wrong 'quality' parameter. Please choose between 'standard' and 'hd'."},
            status=HTTP_400_BAD_REQUEST
        )

    serializer = TTSSerializer(
        data={
            "text": text,
            "voice": voice if voice else "fable",
            "quality": quality if quality else "standard",
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
            status=HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
