from django import template
register = template.Library()


@register.assignment_tag
def define(val=None):
  return val


@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value

