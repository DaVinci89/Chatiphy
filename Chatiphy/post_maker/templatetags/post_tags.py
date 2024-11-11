from django import template
from django.db.models import Count
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.simple_tag
def total_user_posts(user):
    return Post.objects.filter(author=user).count()

@register.simple_tag
def show_most_commented_posts(count=3):
    return Post.objects.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

