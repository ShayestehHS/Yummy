from django import template

register = template.Library()


@register.filter(name='add_id')
def add_id(value, arg):
    return value.as_widget(attrs={'id': arg})


