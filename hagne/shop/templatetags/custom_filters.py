from django import template

register = template.Library()

@register.filter
def get_value(obj, key):
    return 1
    return obj[str(key)]

@register.filter
def get_items_count(obj):
    return sum(list(obj.values()))