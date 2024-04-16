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
    if not text:
        return Response({"error": "Please provide 'text' argument in the request."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TTSSerializer(data={'text': text})

    if serializer.is_valid():
        validated_text = serializer.validated_data.get("text")
        tts = OpenTTS(validated_text)
        audio_obj = tts.speech_for_api()  # Model OBJ with file field

        return Response({"file": audio_obj.audio_file.url}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
