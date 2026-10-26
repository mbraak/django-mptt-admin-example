from django.contrib.auth import get_user_model, login


class AutoLoginMiddleware:
    """Log every visitor in as the demo `admin` user. Only enabled when DEBUG is on."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            user = get_user_model().objects.filter(username="admin").first()
            if user:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
        return self.get_response(request)
