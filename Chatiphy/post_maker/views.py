from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>CHATIPHY</h1><br><p><b>Main Page</b></p>")

def group_posts(request, page):
    return HttpResponse(f"<h1>CHATIPHY</h1><br><p>Posts filtered by Groups</p><br><b><i>{page}</i></b>")
