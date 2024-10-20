from django.urls import path
from . import views

app_name = "post_maker"

urlpatterns = [
    path("", views.index, name="index"),
    path("groups/", views.group_posts, name="group_posts"),
    path("groups/<slug:page>", views.group_posts_page, name="group_page"),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback/success/", views.feedback_success, name="feedback_success"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("posts/<int:post_id>/comment", views.add_comment, name="add_comment"),
    path("posts/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("create_post/", views.create_post, name="create_post")
]