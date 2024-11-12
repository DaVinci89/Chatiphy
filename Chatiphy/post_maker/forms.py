from django import forms
from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "group", "image", "tag"]
        widgets = {"text": forms.Textarea(attrs={"placeholder":"Your message..."})}

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "image"]
        widgets = {
            "text": forms.Textarea(attrs={"name":"comment", "id":"comment","placeholder":"Wright your comment here...", "required":"True"}),
        }
        