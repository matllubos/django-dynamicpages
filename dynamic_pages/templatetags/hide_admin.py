# coding: utf-8
from django import template

register = template.Library()

@register.filter
def has_model(app_models):
    for model in app_models:
        if not model['perms'].has_key('list_hide'):
            return True
    return False    