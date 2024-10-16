from django import forms
from .models import Post, Group
from .validators import validate_not_empty


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, validators=[validate_not_empty, ])
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    is_answered = forms.BooleanField()

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "group", "image"]
        widgets = {"text": forms.Textarea(attrs={"placeholder":"Your message..."})}
        