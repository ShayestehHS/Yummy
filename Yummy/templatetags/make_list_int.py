from django import template

register = template.Library()


@register.filter(name='make_list_int')
def make_list_int(value):
    template_list = []
    list_int= list(value)
    for item in list_int:
        template_list.append(int(item))
    return template_list