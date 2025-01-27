from django.urls import path
from . import views

app_name = "post_maker"

urlpatterns = [
    path("", views.index, name="index"),
    path("tag/<slug:tag_slug>/", views.index, name="index_by_tag"),
    path("search/", views.search_field, name="search_field"),
    path("search/<slug:tag_slug>/", views.search_field, name="search_field_by_tag"),
    path("groups/", views.group_posts, name="group_posts"),
    path("groups/<slug:page>", views.group_posts_page, name="group_page"),
    path("groups/<slug:page>/<slug:tag_slug>/", views.group_posts_page, name="group_page_by_tag"),
    path("posts/<int:post_id>/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/<int:post_id>/comment", views.add_comment, name="add_comment"),
    path("posts/<int:post_id>/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("create_post/", views.create_post, name="create_post"),
    path("posts/<int:pk>", views.get_post, name="get_post_api"),
    path("group/<slug:page>/", views.get_group, name="get_group_api"),
    path("comments/<int:post_id>/", views.get_comment, name="get_comment_api")

]