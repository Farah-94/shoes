import os
from django import template

register = template.Library()

@register.filter
def basename(image_field):
    """
    Given an ImageField (or a path string), return just the filename.
    """
    # image_field.name is e.g. "store/gallery/heels.png"
    name = getattr(image_field, "name", image_field)
    return os.path.basename(str(name))
