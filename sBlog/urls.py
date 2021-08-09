from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("login_success", views.logged_in, name="login_success"),
    path("logout", views.logout, name="logout"),
    path("new_post", views.post, name="new post"),
    path("info", views.about, name="site info"),
    path("view/<str:post_id>", views.view_post, name="view post"),
    path("history", views.post_history, name="user post history"),
    path("search", views.search, name="search"),
    path("comment/<str:post_id>", views.comment, name="comment on post"),
    path("comment_success/<str:post_id>", views.comment_success, name="successful comment"),
    path("edit/<str:post_id>", views.edit_post, name="edit post"),
    path("delete/<str:post_id>", views.delete_post, name="delete post")
]