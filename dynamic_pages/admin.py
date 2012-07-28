# coding: utf-8
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_models
from django.conf import settings

from utilities.admin.admin import UpdateRelatedAdmin, HiddenModelAdmin

from form.page import PageForm
from models import Page, Meta, PageContent

class ChangeTree(ChangeList):
    
    
    def tree_sort(self, parent):
        result = []
        for obj in self.result_list.filter(parent = parent).order_by('order'):
            result = result + [obj.id] + self.tree_sort(obj)
        return result
    
    def get_depth(self, obj):
        depth = 0
        parent =  getattr(obj, self.model_admin.parent)
        obj.parent
        while(parent != None):
            parent = getattr(parent, self.model_admin.parent)
            depth += 1
        return depth
    
class TreeModelAdmin(UpdateRelatedAdmin):
    
    parent = None
    change_list_template = 'admin/change_tree.html'
    
    def queryset(self, request):
        qs = super(TreeModelAdmin, self).queryset(request)
        
        for obj in qs:
            obj.depth = 0
        return qs
    
    def get_changelist(self, request, **kwargs):
        return ChangeTree 
    
    
class PageAdmin(TreeModelAdmin):
    list_display = ('title','absolute_url','url', 'page_type', 'order')
    form = PageForm
    parent = 'parent'
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs): 
        sites = super(PageAdmin, self).formfield_for_foreignkey(db_field, request=None, **kwargs)
        if db_field.name == self.parent: 
            sites.queryset = Page.objects.filter(parent__isnull=True) | Page.objects.filter(parent__in = Page.objects.filter(parent__isnull=True)).exclude(parent=self.get_obj(request))
        return sites
    
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


def autoregister():
    for model in get_models():
        if(issubclass(model, PageContent)):
            try:
                admin.site.register(model, HiddenModelAdmin)
            except AlreadyRegistered:
                pass
autoregister()