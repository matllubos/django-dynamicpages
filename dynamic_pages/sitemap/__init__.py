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
        
    
class DefaultPageSitemap(Sitemap):

    def __init__(self, page, data = []):
        self.page = page
        self.data = data
        
    def items(self):
        items = []
       
        from dynamic_pages.dynamic.utils import get_dynamic_url_by_choice
       
        dynamic_url = get_dynamic_url_by_choice(self.page.page_type)
        i = 0
        for pattern in dynamic_url.get_patterns(self.page):     
            pattern = re.sub('^\^', '', pattern) 
            pattern = re.sub('\$$', '', pattern) 
            pattern = re.sub('/\?', '', pattern) 

            if not re.search('[\[\?\+\*\.\]]', pattern):
                pattern = re.sub('[\(\)]', '', pattern)
                items.append(SitemapUrl(self.page.updated, pattern))
            elif len(self.data) > i:
                items.extend(self.data[i].get_sitemaps(pattern, self.page.updated))
                i+=1
                    
        return items

    
    def _get_paginator(self):
        return paginator.Paginator(self.items(), self.limit)
    paginator = property(_get_paginator)
    
    def lastmod(self, obj):
        return obj.updated
    
    def location(self, obj):
        return '/%s' % obj.url