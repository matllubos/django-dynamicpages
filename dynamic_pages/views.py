# coding: utf-8
from django.views.generic.base import TemplateView

class StaticView(TemplateView):
    template_name = 'static.html'