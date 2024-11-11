from django import template
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()

@register.simple_tag
def total_user_posts(user):
    return Post.objects.filter(author=user).count()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

