from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse


def home(request):
    return HttpResponse("Hello, World!")


def login_user(request):
    print("FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            response = redirect(reverse("notes:login_user"))
            response.set_cookie("auth_token", user.password, httponly=True, secure=True)
            return response
        else:
            return render(
                request, "notes/login_page.html", {"error": "Invalid credentials"}
            )

    return render(request, "notes/login_page.html")


def logout_user(request):
    response = JsonResponse({"message": "Logged out"})
    response.delete_cookie("auth_token")
    return response


def protected(request):
    auth_token = request.COOKIES.get("auth_token")
    if auth_token:
        return redirect("/protected/notes/")
    return redirect("/login/")


def notes(request):
    return HttpResponse("Hello, Notes!")


def login_page(request):
    return render(request, "notes/login_page.html")
