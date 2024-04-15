from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.response import Response

from website.models import Narration
from .serializers import NarrationSerializer


class NarrationsViewSet(viewsets.ModelViewSet):
    queryset = Narration.objects.all()
    serializer_class = NarrationSerializer

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
