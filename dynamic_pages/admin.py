# coding: utf-8
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import get_models
from django.conf import settings

from utilities.admin import TreeModelMixin, RelatedToolsAdmin, HiddenModelAdmin

from forms.page import PageForm
from models import Page, Meta, PageContent
from django.contrib.sites.models import Site
from django.utils.encoding import smart_unicode
from dynamic_pages.dynamic.utils import get_dynamic_url_choices
from django.http import HttpResponseRedirect

    
class PageAdmin(TreeModelMixin, RelatedToolsAdmin):
    list_display = ('title','absolute_url','url', 'page_type', 'publish_on', 'order')
    list_filter = ('publish_on', )
    
    form = PageForm
    parent = 'parent'
    
    exclude = ('publish_on', )
    change_list_template = 'admin/page_change_list.html'
    change_form_template = 'admin/page_change_form.html'
    
    def changelist_view(self, request, extra_context={}):
        request_get = request.GET.copy()
        if not request_get.has_key('publish_on__id__exact'):
            request_get['publish_on__id__exact'] = smart_unicode(settings.SITE_ID)
        request.GET = request_get
        
        return super(PageAdmin, self).changelist_view(request, extra_context)
    
    def add_view(self, request, form_url='', extra_context={}):
        extra_context['site_id'] = self.get_site_id(request)
        return super(PageAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context={}):
        extra_context['site_id'] = self.get_object(request, object_id).publish_on.pk
        return super(PageAdmin, self).change_view(request, object_id, extra_context)
    
    def get_obj(self, request):
        object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            object_id = int(object_id)
        except ValueError:
            return None
        return Page.objects.get(pk=object_id)
    
    def save_form(self, request, form, change):
        super(PageAdmin, self).save_form(request, form, change)       
        new_obj = form.save(commit=False)
        new_obj.publish_on = Site.objects.get(pk = self.get_site_id(request))
        return new_obj
    
    def get_site_id(self, request):
        obj = self.get_obj(request)
        if obj:
            return obj.publish_on.pk
        if request.GET.has_key('site'):
            return int(request.GET['site'])
        return settings.SITE_ID
      
    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        if db_field.name == 'page_type':
            kwargs['choices'] = [('', '---------')] + get_dynamic_url_choices(site = self.get_site_id(request))
        return db_field.formfield(**kwargs) 
        
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'parent':
            field.queryset = field.queryset.filter(publish_on = self.get_site_id(request))
        return field
    
    def response_change(self, request, obj):
        response = super(PageAdmin, self).response_change(request, obj)
        if isinstance(response, HttpResponseRedirect):
            if response['Location'] == '../':
                response['Location'] += '?publish_on__id__exact=%s' % obj.publish_on.pk
            elif '?' in response['Location']:
                response['Location'] += '&site=%s' % obj.publish_on.pk
            elif response['Location'] != '../../../':
                response['Location'] += '?site=%s' % obj.publish_on.pk
        return response
    
    
    def response_add(self, request, obj):
        response = super(PageAdmin, self).response_add(request, obj)
        if isinstance(response, HttpResponseRedirect):
            if response['Location'] == '../':
                response['Location'] += '?publish_on__id__exact=%s' % obj.publish_on.pk
            elif '?' in response['Location']:
                response['Location'] += '&site=%s' % obj.publish_on.pk
            elif response['Location'] != '../../../':
                response['Location'] += '?site=%s' % obj.publish_on.pk
        return response
         
    def delete_view(self, request, object_id, extra_context={}):
        obj = self.get_object(request, object_id) 
        response = super(PageAdmin, self).delete_view(request, object_id, extra_context)
        if isinstance(response, HttpResponseRedirect):    
            if response['Location'] == '../../':
                response['Location'] += '?publish_on__id__exact=%s' % obj.publish_on.pk
                return response
        return response
            
            
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