import re
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

EXEMPT_URLS = []
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if path == 'accounts/logout':
            logout(request)

        if not request.user.is_authenticated and not url_is_exempt:
            return redirect('startpage')

        if request.user.is_authenticated and url_is_exempt:
            return redirect('chat:chat')
