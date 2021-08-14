from django import template

register = template.Library()


@register.filter
def index(IndexAble, i):
    """
    Return the index <<i>> of indexable.

    For an integer, it's a list of digits.
    For a string, it's a list of characters.

    << i >> should start with << 1 >> not << 0 >>
    """
    return IndexAble[i-1]
