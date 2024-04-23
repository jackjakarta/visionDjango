from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the current host starts with www.
        if request.get_host().startswith('www.'):
            # Replace 'www.' with nothing and get the new host
            new_host = request.get_host().replace('www.', '')
            # Build new URL
            new_url = request.build_absolute_uri().replace(request.get_host(), new_host)
            # Permanent redirect to the new URL without www
            return HttpResponsePermanentRedirect(new_url)

        response = self.get_response(request)
        return response
