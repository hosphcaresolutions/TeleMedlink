from django import template

register = template.Library()

@register.filter
def get_item(obj, key):
    try:
        if isinstance(obj, dict):
            return obj.get(key, 0)
        elif isinstance(obj, list):
            return obj[int(key)] if len(obj) > int(key) else 0
    except (ValueError, IndexError, TypeError):
        return 0
