import typing

from django.http import HttpRequest
from rest_framework import authentication, exceptions
from rest_framework_api_key.permissions import BaseHasAPIKey

from users.models import UserAPIKey


class IsAPIKeyUser(BaseHasAPIKey):
    model = UserAPIKey

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, obj: typing.Any
    ) -> bool:
        # First, call the base implementation to ensure the API key itself is valid
        if not super().has_permission(request, view):
            return False

        # Get the API key from the request
        key = self.get_key(request)
        if not key:
            return False

        # Retrieve the APIKey instance based on the key provided in the request
        try:
            api_key = self.model.objects.get_from_key(key)
        except self.model.DoesNotExist:
            return False

        # Now, ensure the user associated with the APIKey is the owner of the object
        # You need to adjust `obj.user` to match the attribute name in your model
        # that refers to the user who owns the resource.
        return obj.user == api_key.user


class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = request.META.get("HTTP_X_API_KEY")  # Adjust the header name as needed
        if not key:
            return None
        try:
            api_key = UserAPIKey.objects.get_from_key(key)
            if api_key is None or not api_key.user:
                raise exceptions.AuthenticationFailed("No such API key")

            return api_key.user, api_key  # Return the user and the API key object
        except UserAPIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such API key")
