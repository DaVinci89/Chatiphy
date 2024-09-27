from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormCreation


class SignUp(CreateView):
    # Define form class
    form_class = FormCreation
    # Redirecting to main page after successful register
    success_url = reverse_lazy("post_maker:index")
    template_name = "users/signup.html"
