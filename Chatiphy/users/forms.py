from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class FormCreation(UserCreationForm):
    """Class for registration form"""

    class Meta(UserCreationForm.Meta):
        # Model User will connect with this form
        model = User
        fields = ("first_name", "last_name", "username", "email")
