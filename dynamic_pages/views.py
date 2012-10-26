# coding: utf-8
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect

from dynamic_pages.models import PageContent

class StaticView(TemplateView):
    template_name = 'static.html'
    
    
def redirect_to_url(request):
    page_content = PageContent.get_content(request.path)
    return HttpResponseRedirect(page_content.url)

def redirect_to_page(request):
    page_content = PageContent.get_content(request.path)
    return HttpResponseRedirect(page_content.page.url)