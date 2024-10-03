from django import forms
from .validators import validate_not_empty


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, validators=[validate_not_empty, ])
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    is_answered = forms.BooleanField()
