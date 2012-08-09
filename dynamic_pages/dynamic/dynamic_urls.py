# coding: utf-8
import re

from django.conf.urls.defaults import url

class DynamicUrl:
    '''
    Dynamic alternative to django url
    '''
    
    def __init__(self, name, verbose_name, view = None, patterns = [], model = None, can_change_url = True, view_kwargs = None):
        self.name = name
        self.view = view
        self.patterns = patterns
        self.model = model
        self.verbose_name = verbose_name
        self.can_change_url = can_change_url
        self.view_kwargs = view_kwargs
    
    def get_model_name(self):
        if not self.model:
            return 'none'
        return self.model.lower()
        
    def get_full_name(self):
        menu = 'nomenu'
        if (self.can_be_in_menu()):
            menu = 'menu'
        change_url = 'false'
        if (self.can_change_url):
            change_url = 'true'
        return '%s-%s-%s-%s' % (self.get_model_name(), self.name, menu, change_url)  
     
    def get_patterns(self, page):
        
        patterns = []
        if (not self.patterns):
            return patterns
        
        for pattern in self.patterns:
            pattern_parts = []
               
            if page.absolute_url != '':
                pattern_parts.append(page.absolute_url)
            
            if pattern != '':
                pattern_parts.append(pattern)
                
            patterns.append(r'^%s/?$'% '/'.join(pattern_parts))
        
        if (page.default):
            patterns.append(r'^/?$')
                
        return patterns
        
    def get_url_patterns(self, page):
        urls = []
        for pattern in self.get_patterns(page):
            urls.append(url(pattern, self.view, kwargs=self.view_kwargs, name=self.name))
        return urls  
           
    def can_be_in_menu(self):
        if (self.name in ('static', 'redirects', 'redirectstourl', 'redirectstopage')):
            return True
        
        for url_pattern in self.patterns:
            if (not re.search('\(.*[\?\|\+\.\*\[\]]+.*\)', url_pattern)):
                return True
        return False
       
    def get_choice(self):
        return (self.get_full_name(), self.verbose_name)
    
       
    def has_model(self):
        return self.model != None
    
    def equals(self, page, path):
        for pattern in self.get_patterns(page):
            if (re.search(pattern, path)):
                return True
        return False