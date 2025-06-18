from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Note
from .models import User


def requires_auth(view_func):
    def wrapper(request, *args, **kwargs):
        auth_token = request.COOKIES.get("auth_token")
        if not auth_token:
            return redirect("/login_page/")
        return view_func(request, *args, **kwargs)

    return wrapper


def home(request):
    auth_token = request.COOKIES.get("auth_token")
    if auth_token:
        return redirect("/notes/")
    else:
        return render(request, "notes/home.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            response = redirect(reverse("notes:home"))
            response.set_cookie("auth_token", user.password, httponly=True, secure=True)
            return response
        else:
            return render(
                request, "notes/login_page.html", {"error": "Invalid credentials"}
            )

    return render(request, "notes/login_page.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            return render(
                request,
                "notes/register_page.html",
                {"error": "All fields are required"},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "notes/register_page.html",
                {"error": "Username already exists"},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request, "notes/register_page.html", {"error": "Email already exists"}
            )

        User.objects.create_user(username, email, password)
        return redirect("/login_page/")
    return render(request, "notes/register_page.html")


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("notes:home"))
    response.delete_cookie("auth_token")
    return response


@requires_auth
def notes(request):
    notes = Note.objects.all().order_by("-created_at")
    return render(request, "notes/notes.html", {"notes": notes})


def login_page(request):
    return render(request, "notes/login_page.html")


def register_page(request):
    return render(request, "notes/register_page.html")


@requires_auth
def create_note(request):
    if request.method == "POST":
        text = request.POST.get("text")

        if not text:
            return JsonResponse({"error": "Note text is required"}, status=400)

        Note.objects.create(text=text, user=request.user)
        return HttpResponseRedirect(reverse("notes:notes"))
    return JsonResponse({"error": "Invalid request method"}, status=405)


@requires_auth
def delete_note(request, note_id):
    if request.method == "POST":
        try:
            note = Note.objects.get(id=note_id)
            if note.user == request.user:
                note.delete()
                return HttpResponseRedirect(reverse("notes:notes"))
            else:
                return JsonResponse(
                    {"error": "You do not have permission to delete this note"},
                    status=403,
                )
        except Note.DoesNotExist:
            return JsonResponse({"error": "Note not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)
