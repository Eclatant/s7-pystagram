import sys

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from raven.contrib.django.raven_compat.models import sentry_exception_handler

from pystagram.sample_exceptions import HelloWorldError



class SimpleMiddleware(MiddlewareMixin):
    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            sentry_exception_handler(request=request)
            ctx = {
                'error': exc,
                'status': 500,
            }
            return render(request, 'error.html', ctx)

    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'

