from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("CHATIPHY\nMain Page")

def group_posts(request):
    return HttpResponse("CHATIPHY\nPosts filtered by Groups")
