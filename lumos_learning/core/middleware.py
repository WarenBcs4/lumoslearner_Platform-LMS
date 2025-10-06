from django.http import HttpResponseTooManyRequests
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if hasattr(exception, 'status_code') and exception.status_code == 429:
            return HttpResponseTooManyRequests("Rate limit exceeded. Please try again later.")