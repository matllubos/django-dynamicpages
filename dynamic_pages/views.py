# coding: utf-8
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import Http404 

class StaticView(TemplateView):
    template_name = 'static.html'