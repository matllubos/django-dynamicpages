# coding: utf-8
from django.conf.urls.defaults import patterns

def get_dynamic_urls():
    from urls import dynamic_patterns
    from dynamic_pages.urls import DEFAULT_DYNAMIC_URLS
    try:
        dynamic_urls = list(dynamic_patterns)
        for default_pattern in DEFAULT_DYNAMIC_URLS:
            if not default_pattern.name in [pattern.name for pattern in dynamic_urls]:
                dynamic_urls.append(default_pattern)
        return dynamic_urls
    except:
        return []
    
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
    from dynamic_pages.models import Page
    urlpatterns = patterns('')
    for page in Page.objects.all():
        if(page.pattern()):
            urlpatterns += page.pattern()
    return urlpatterns