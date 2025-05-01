from django import template

register = template.Library()

@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class':css})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def count_likes(post):
    return post.likes_dislikes.filter(is_like=True).count()

@register.filter
def count_dislikes(post):
    return post.likes_dislikes.filter(is_like=False).count()