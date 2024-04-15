from django.contrib.auth import get_user_model
from rest_framework import serializers

from website.models import Narration, Video

AuthUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        exclude = [
            "id",
            'first_name',
            'last_name',
            "last_login",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        ]


class NarrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all(), required=False)

    class Meta:
        model = Narration
        exclude = ["created_at", "updated_at", ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user
        if user:
            representation['user'] = UserSerializer(user).data

        return representation
