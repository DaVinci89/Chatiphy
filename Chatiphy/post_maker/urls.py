from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("group/<slug:page>", views.group_posts),
    path("group/", views.group_posts)
]