from django import template

register = template.Library()

@register.filter
def get_value(obj, key):
    return getattr(obj, key, "")