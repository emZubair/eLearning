from django import template

register = template.Library()


@register.filter
def model_name(obj):
    # import pdb
    # pdb.set_trace()
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
