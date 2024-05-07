from django import template

register = template.Library()

@register.filter(name='add_a_or_an')
def add_a_or_an(value):
    """Adds 'a' or 'an' before a word based on its first letter."""
    if value[0].lower() in 'aeiou':
        return f'an {value}'
    else:
        return f'a {value}'