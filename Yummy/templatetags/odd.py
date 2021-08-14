from django import template

register = template.Library()


@register.filter(name='odd')
def odd(value, i):
    return value % i
