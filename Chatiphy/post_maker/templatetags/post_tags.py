from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.simple_tag
def total_user_posts(user):
    return Post.objects.filter(author=user).count()

