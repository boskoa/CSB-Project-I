from django.urls import path
from . import views

app_name = "notes"
urlpatterns = [
    path("", views.home, name="home"),
    path("login_page/", views.login_page, name="login_page"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("protected/", views.protected, name="protected"),
    path("protected/notes/", views.notes, name="notes"),
]
