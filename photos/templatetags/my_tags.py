from django import template
from django.template.base import VariableNode
from django.contrib.auth import get_user_model


register = template.Library()


@register.filter
def did_like(post, user):
    return post.like_set.filter(user=user).exists()


@register.tag(name='addnim')
def add_nim(parser, token):
    nodelist = parser.parse(['end_add_nim', 'endaddnim', ])
    parser.delete_first_token()
    return NimNode(nodelist)


class NimNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        self.user_class = get_user_model()

    def render(self, context):
        output = []
        for node in self.nodelist:
            if not isinstance(node, VariableNode):
                output.append(node.render(context))
                continue
            obj = node.filter_expression.resolve(context)

            if not isinstance(obj, self.user_class):
                output.append(node.render(context))
                continue

            result = '{}님'.format(node.render(context))
            output.append(result)

        return ''.join(output)

