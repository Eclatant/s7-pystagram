import sys
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render

from pystagram.sample_exceptions import HelloWorldError

from raven import Client

client = Client('https://197093fb157044a1a1a9e0960d89bc03:af5d77eb13e84b3bbfecdea05e5d7ef4@sentry.io/102943')



class SimpleMiddleware(MiddlewareMixin):
    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            client.captureException(sys.exc_info)
            ctx = {
                'error': exc,
                'status': 500,
            }
            return render(request, 'error.html', ctx)

    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'

