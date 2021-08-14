from django import template

register = template.Library()


@register.simple_tag
def url_replace(path, param, value):
    # print(f"Value=>{value}\nField=>{param}\nUrl=>{path}")
    return path.replace(f"/{param}/", f"/{value}/")
