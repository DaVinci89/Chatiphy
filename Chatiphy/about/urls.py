from django.urls import path
from . import views

app_name = "about"

urlpatterns = [
        path("author/", views.AboutAuthorView.as_view(), name="author"),
        path("tech/", views.AboutTechView.as_view(), name="tech"),
        path("feedback/", views.feedback, name="feedback"),
        path("feedback/success/", views.feedback_success, name="feedback_success"),
        ]