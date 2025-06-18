from django.urls import path
from . import views

app_name = "notes"
urlpatterns = [
    path("", views.home, name="home"),
    path("login_page/", views.login_page, name="login_page"),
    path("login_user/", views.login_user, name="login_user"),
    path("register_page/", views.register_page, name="register_page"),
    path("register_user/", views.register_user, name="register_user"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("notes/", views.notes, name="notes"),
    path("create_note/", views.create_note, name="create_note"),
    path("delete_note/<int:note_id>/", views.delete_note, name="delete_note"),
]
