from django import template


register = template.Library()


@register.filter
def did_like(post, user):
    return post.like_set.filter(user=user).exists()

