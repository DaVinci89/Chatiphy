from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    template = "post_maker/index.html"
    text = "<b>This will be the main page of the project.</b>"
    context = {
        "descr":text,
    }
    return render(request, template, context)

def group_posts(request):
    template = "post_maker/group_posts.html"
    text = "<b>There will be information about groups of the project Chatiphy</b>"
    context = {
        "descr":text,
    }
    return render(request, template, context)

def group_posts_page(request, page):
    template = "post_maker/group_posts_page.html"
    text = "<b>There will be information about group chosen by the user</b>"
    context = {
        "page":page,
        "descr":text,
    }
    return render(request, template, context)
