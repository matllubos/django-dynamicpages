# coding: utf-8
import re

from django.contrib.sitemaps import Sitemap

from django.utils.encoding import smart_unicode, force_unicode
from django.core import urlresolvers, paginator

from dynamic_pages.models import Page
from django.core.cache import get_cache


class Siteurls(object):
    
    def get_urls(self, pattern):
        return []

    def get_sitemaps(self, pattern, updated):
        urls = self.get_urls(pattern)
        for url in urls:
            if not re.search('[\[\?\+\*\.\]]', url):
                url = re.sub('[\(\)]', '', url)
                yield SitemapUrl(updated, url)
    

class ModelFieldSiteurls(Siteurls):
    def __init__(self, queryset, field='pk'):
        self.queryset = queryset
        self.field = field
        
    def get_sitemaps(self, pattern, updated):
        for obj in self.queryset.all():
            url = re.sub('(\([^)]*\))', smart_unicode(getattr(obj, self.field)), pattern, count=1)
            if not re.search('[\[\?\+\*\.\]]', url):
                url = re.sub('[\(\)]', '', url)
                yield SitemapUrl(updated, url)
    
class SitemapUrl(object):
    def __init__(self, updated, url):
        self.updated = updated
        self.url = url
        

class StaticPagesSitemap(Sitemap):

    def __init__(self, data={}):
        self.data = data
        
    def items(self):
        items = []
       
        from dynamic_pages.dynamic.utils import get_dynamic_url_by_choice
        
        for page in Page.objects.all().order_by('parent', 'order'):
            dynamic_url = get_dynamic_url_by_choice(page.page_type)
            i = 0
            for pattern in dynamic_url.get_patterns(page):     
                pattern = re.sub('^\^', '', pattern) 
                pattern = re.sub('\$$', '', pattern) 
                pattern = re.sub('/\?', '', pattern) 

                if not re.search('[\[\?\+\*\.\]]', pattern):
                    pattern = re.sub('[\(\)]', '', pattern)
                    items.append(SitemapUrl(page.updated, pattern))
                elif self.data.has_key(page.page_type_name) and len(self.data[page.page_type_name]) > i:
                    items.extend(self.data[page.page_type_name][i].get_sitemaps(pattern, page.updated))
                    i+=1
                    
        return items

    
    def _get_paginator(self):
        return paginator.Paginator(self.items(), self.limit)
    paginator = property(_get_paginator)
    
    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return '/%s' % obj.url