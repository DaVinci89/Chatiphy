from django.shortcuts import render

def page_not_found(request, exception):
    template = "core/404.html"
    return render(request, template, {"path":request.path}, status=404)