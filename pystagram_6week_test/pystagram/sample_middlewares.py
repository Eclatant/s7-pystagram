from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render

from .sample_exceptions import HelloWorldError

class SampleMiddleware(MiddlewareMixin):
    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            # 첫번째 인자가 두번째 클래스를 통해서 만들어진 것인지 확인함
            ctx ={
                'error': exc,
                'status':500,
            }
            return render(request, 'error.html', ctx)

    def process_request(self, request):
        request.just_say = 'Lorem Ipsum'

