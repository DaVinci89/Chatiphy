from django.shortcuts import render

def page_not_found(request, exception):
    template = "core/404.html"
    return render(request, template, {"path":request.path}, status=404)

def bad_request(request, exception):
    template = "core/400.html"
    return render(request, template, status=400)

def forbidden(request, exception):
    template = "core/403.html"
    return render(request, template, status=403)

def server_error(request):
    template = "core/500.html"
    return render(request, template, status=500)

def unavailable(request, exception):
    template = "core/503.html"
    return render(request, template, status=503)
