# coding: utf-8
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import get_models

from utilities.admin import TreeModelMixin, RelatedToolsAdmin, HiddenModelAdmin

from form.page import PageForm
from models import Page, Meta, PageContent
    
class PageAdmin(TreeModelMixin, RelatedToolsAdmin):
    list_display = ('title','absolute_url','url', 'page_type', 'order')
    form = PageForm
    parent = 'parent'
    
   
    
    def get_obj(self, request):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id = int(object_id)
        except ValueError:
            return None
        return Page.objects.get(pk=object_id)
    
    class Media:
        js = (
            '/static/dynamic_pages/js/jquery-1.6.4.min.js',
            '/static/dynamic_pages/js/pages.js'
        )

admin.site.register(Page, PageAdmin)            
admin.site.register(Meta, HiddenModelAdmin)   

def autoregister():
    '''
    Automatic registration PageContent models to admin
    '''
    for model in get_models():
        if(issubclass(model, PageContent)):
            try:
                admin.site.register(model, HiddenModelAdmin)
            except AlreadyRegistered:
                pass
autoregister()