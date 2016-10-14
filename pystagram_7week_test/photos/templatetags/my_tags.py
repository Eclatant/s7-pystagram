from django import template
from django.template.base import VariableNode
from django.contrib.auth import get_user_model
from profiles.models import Profile
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter
def did_like(photo, user):
    return photo.like_set.filter(user=user).exists()

@register.filter
def did_follow(following, follower):
    profile = get_object_or_404(Profile, pk=follower)
    return profile.follow_set.filter(user=following).exists()

@register.tag(name='addnim')
def add_nim(parser, token):
    nodelist = parser.parse(['endaddnim',])
    parser.delete_first_token()
    return NimNode(nodelist)

class NimNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        self.user_class = get_user_model()

    def render(self, context):
        #context는 view에서 넘겨주는 ctx dictionary 값
        outputs = []
        for node in self.nodelist:
            if not isinstance(node, VariableNode):
                outputs.append(node.render(context))
                continue

            obj = node.filter_expression.resolve(context)
            if not isinstance(obj, self.user_class):
                outputs.append(node.render(context))
                continue
            
            result = '{}님'.format(node.render(context))
            outputs.append(result)

        return ''.join(outputs)


