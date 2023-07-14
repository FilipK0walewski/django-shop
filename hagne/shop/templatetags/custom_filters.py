from django import template

register = template.Library()

@register.filter
def get_value(obj, key):
    return obj[str(key)]

@register.filter
def get_items_count(obj):
    if isinstance(obj, dict) is False:
        return 0
    if 'items' not in obj:
        return 0
    return sum(list(obj['items'].values()))


@register.filter
def to_string(obj):
    return str(obj)


@register.filter
def multiply(obj, n):
    return obj * n


@register.filter
def category_map(obj):
    return '<ul><li>123</li></ul>'


@register.filter
def second_to_last(obj: list):
    if isinstance(obj, list) is False:
        return None
    if len(obj) < 2:
        return None
    return obj[-2]


@register.filter
def search_params(get):
    res = []
    for k, v in get.items():
        if k == 'page':
            continue    
        res.append(f'{k}={v}')
    return '&'.join(res)