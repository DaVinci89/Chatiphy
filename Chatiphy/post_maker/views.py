from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    template = "post_maker/index.html"
    posts = Post.objects.order_by("-pub_date")[:10]
    context = {
        "posts": posts,
    }
    return render(request, template, context)


def group_posts(request):
    template = "post_maker/group_posts.html"
    text = "<h2><b>Groups</b><h2>"
    groups = Group.objects.all()[:10]
    context = {
        "header": text,
        "groups": groups,
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
