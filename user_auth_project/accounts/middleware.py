from django.shortcuts import redirect
from django.utils import timezone

class LockoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lockout_time = request.session.get("lockout_time")

        if lockout_time and timezone.now() < lockout_time:
            if request.path not in ["/accounts/login/", "/accounts/lockout/"]:
                return redirect("lockout")  # ロックアウトページへリダイレクト

        return self.get_response(request)