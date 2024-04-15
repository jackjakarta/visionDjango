from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets

from website.models import Narration
from .serializers import NarrationSerializer


class NarrationViewSet(viewsets.ModelViewSet):
    queryset = Narration.objects.all()
    serializer_class = NarrationSerializer

    def get_queryset(self):
        if not isinstance(self.request.user, AnonymousUser):
            user_id = self.request.user.id

            return Narration.objects.filter(user_id=user_id)
