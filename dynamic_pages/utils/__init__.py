# coding: utf-8
import re

from django.contrib.admin.util import quote as django_quote, unquote as django_unquote
from django.utils.encoding import force_unicode

def quote(url):
    url = django_quote(url)
    return re.sub(r' ', '__', url)

def unquote(url):
    url = re.sub(r'__', ' ', force_unicode(url))
    return django_unquote(url)