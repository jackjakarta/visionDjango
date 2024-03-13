from django.shortcuts import reverse, redirect, Http404, get_object_or_404

from django.utils import timezone
from users.models import Activation


class ActivationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        token = view_kwargs.get('token')
        activation = get_object_or_404(Activation, token=token, activated_at=None)
        reset_token_route = reverse('users:activation:reset_token', args=(token, ))
        is_reset_token_request = reset_token_route == request.path

        if activation.expires_at < timezone.now():
            if not is_reset_token_request:
                return redirect(reset_token_route)
        elif is_reset_token_request:
            raise Http404('Token is still active!')
