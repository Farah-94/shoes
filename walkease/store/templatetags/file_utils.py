import os
from django import template

register = template.Library()

@register.filter
def basename(path):
    """Return the filename portion of a path."""
    return os.path.basename(path or "")