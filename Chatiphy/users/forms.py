from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class FormCreation(UserCreationForm):
    """Class for registration form"""

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already exists.")
        return email

    class Meta(UserCreationForm.Meta):
        # Model User will connect with this form
        model = User
        fields = ("first_name", "last_name", "username", "email")
