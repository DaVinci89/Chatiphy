from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Post.objects.filter(text__contains=keyword).select_related("author")
    else:
        posts = Post.objects.order_by("-pub_date")[:10]
    template = "post_maker/index.html"
    context = {
        "posts": posts,
    }
    return render(request, template, context)


def group_posts(request):
    template = "post_maker/group_posts.html"
    text = "<h2><b>Groups</b><h2>"
    groups = Group.objects.all()[:10]
    groups_count = Group.objects.count()
    context = {
        "header": text,
        "groups": groups,
        "groups_count":groups_count
    }
    return render(request, template, context)


def group_posts_page(request, page):
    template = "post_maker/group_posts_page.html"
    group = get_object_or_404(Group, slug=page)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    context = {
        "group": group,
        "posts": posts,
    }
    return render(request, template, context)
