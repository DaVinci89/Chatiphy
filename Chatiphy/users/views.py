from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormCreation
from django.contrib.auth import logout
from django.shortcuts import render


class SignUp(CreateView):
    # Define form class
    form_class = FormCreation
    # Redirecting to main page after successful register
    success_url = reverse_lazy("post_maker:index")
    template_name = "users/signup.html"
    
def logout_view(request):
    logout(request)
    context = {}
    return render(request, "users/logged_out.html", context)
