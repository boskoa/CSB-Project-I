from django.shortcuts import redirect


class ProtectedRoutesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/protected") and not request.COOKIES.get(
            "auth_token"
        ):
            return redirect("/login/")
        return self.get_response(request)
