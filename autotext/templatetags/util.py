# app/templatetags/util.py
from django import template

register = template.Library()


@register.filter
def get_type(obj):
    return type(obj)
