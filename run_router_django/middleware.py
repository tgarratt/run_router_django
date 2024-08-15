# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware, get_token

class LogCsrfTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        expected_csrf_token = get_token(request)
        print(f"Expected CSRF Token: {expected_csrf_token}")
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        return None
