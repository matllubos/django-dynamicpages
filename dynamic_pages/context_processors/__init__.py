# coding: utf-8
from dynamic_pages.models import PageContent

def page_content(request):
    return {'page_content': PageContent.get_content(request.path)}