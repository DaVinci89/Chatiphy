from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    template = "../templates/post_maker/index.html"
    return render(request, template)

def group_posts(request, page=None):
    template = "../templates/post_maker/group_posts.html"
    return render(request, template)
