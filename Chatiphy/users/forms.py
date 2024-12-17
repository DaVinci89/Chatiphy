from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'date_of_birth', 'location', 'bio', 'profile_image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
