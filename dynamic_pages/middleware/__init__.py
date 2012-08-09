# coding: utf-8
import sys

from datetime import datetime
from django.utils import translation
from django.conf import settings

from dynamic_pages.models import Page

class UrlsReloadMiddleware(object):
    '''
    Automatically updates urls.py
    '''
    
    last_reload = None
    count_pages = 0
    
    def process_request(self, request):
        if not self.last_reload or Page.objects.all().count() != self.count_pages or Page.objects.filter(updated__gte = self.last_reload):
            urlconf = settings.ROOT_URLCONF
            if urlconf in sys.modules:
                reload(sys.modules[urlconf])
        
            self.count_pages = Page.objects.all().count()
            self.last_reload = datetime.now()

        