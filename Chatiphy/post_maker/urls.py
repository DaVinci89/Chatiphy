from django.urls import path
from . import views

app_name = "post_maker"

urlpatterns = [
    path("", views.index, name="index"),
    path("groups/", views.group_posts, name="group_posts"),
    path("groups/<slug:page>", views.group_posts_page, name="group_page"),
    path("feedback/", views.feedback, name="feedback")
]