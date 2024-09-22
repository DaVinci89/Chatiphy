from django.urls import path
from . import views

app_name = "post_maker"

urlpatterns = [
    path("", views.index, name="index"),
    path("groups/<slug:page>", views.group_posts_page),
    path("groups/", views.group_posts, name="group_posts")
]