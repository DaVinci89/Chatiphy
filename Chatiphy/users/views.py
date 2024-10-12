from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormCreation
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render


class SignUp(CreateView):
    # Define form class
    form_class = FormCreation
    # Redirecting to main page after successful register
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"

    def form_valid(self, form):
        return super().form_valid(form)

class PasswordReset(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        error_message = False
        if not User.objects.filter(email=email).exists():
            error_message = True
            return render(self.request, self.template_name, {"form":form, "error_message":error_message})
        return super().form_valid(form)
    
def logout_view(request):
    logout(request)
    context = {}
    return render(request, "users/logged_out.html", context)
