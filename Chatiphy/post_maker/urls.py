from django.urls import path
from . import views

app_name = "post_maker"

urlpatterns = [
    path("", views.index, name="index"),
    path("tag/<slug:tag_slug>/", views.index, name="index_by_tag"),
    path("groups/", views.group_posts, name="group_posts"),
    path("groups/<slug:page>", views.group_posts_page, name="group_page"),
    path("groups/<slug:page>/<slug:tag_slug>/", views.group_posts_page, name="group_page_by_tag"),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback/success/", views.feedback_success, name="feedback_success"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/<slug:tag_slug>/", views.profile, name="profile_by_tag"),
    path("profile/<str:username>/subscribe", views.subscribe, name="subscribe"),
    path("profile/<str:username>/unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("posts/<int:post_id>/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/<int:post_id>/comment", views.add_comment, name="add_comment"),
    path("posts/<int:post_id>/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("create_post/", views.create_post, name="create_post")
]