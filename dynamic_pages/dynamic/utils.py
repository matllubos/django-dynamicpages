# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns

from dynamic_pages.views import StaticView
from dynamic_urls import DynamicUrl
    
DEFAULT_DYNAMIC_URLS = (
    DynamicUrl('static', _(u'Static page'),  StaticView.as_view(), (r'',), 'dynamic_pages.StaticPageContent'),
    DynamicUrl('redirects', _(u'Redirect to first child page')),
    DynamicUrl('redirectstourl', _(u'Redirect to URL'), None, None, 'dynamic_pages.RedirectToURLPageContent', can_change_url = False),
    DynamicUrl('redirectstopage', _(u'Redirect to page'), None, None, 'dynamic_pages.RedirectToPagePageContent', can_change_url = False),
)

def get_dynamic_urls():
    from generic_urls import dynamic_patterns
    return DEFAULT_DYNAMIC_URLS + dynamic_patterns

def get_dynamic_url(name):
    for dynamic_url in get_dynamic_urls():
        if (dynamic_url.name == name):
            return dynamic_url
    return None
        
def get_dynamic_url_by_choice(choice):
    name = choice.split('-')[1]
    return get_dynamic_url(name)

def get_dynamic_url_choices():
    choices = []
    for dynamic_url in get_dynamic_urls():
        choices.append(dynamic_url.get_choice())
    return choices   

def dynamic_urlpatterns():
    from pages.models import Page
    urlpatterns = patterns('')
    for page in Page.objects.all():
        if(page.pattern()):
            urlpatterns += page.pattern()
    return urlpatterns