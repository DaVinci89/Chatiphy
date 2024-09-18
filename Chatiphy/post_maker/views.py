from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("CHATIPHY<br>Main Page")

def group_posts(request, page):
    return HttpResponse(f"CHATIPHY<br>Posts filtered by Groups<br>{page}")
