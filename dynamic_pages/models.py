# coding: utf-8
import re
import sys

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode 
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser

from dynamic.utils import get_dynamic_url_choices, get_dynamic_url_by_choice
from utilities.models.fields import PageTitleField, PageUrlField, HtmlField, PhoneField, OrderField #@UnresolvedImport

last_reload = None
count_pages = 0

def reload_urlconf(urlconf=None):
    global last_reload
    global count_pages
    if not last_reload or Page.objects.all().count() != count_pages or Page.objects.filter(updated__gte = last_reload):
        print reload
        if urlconf is None:
            urlconf = settings.ROOT_URLCONF
        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
        
        count_pages = Page.objects.all().count()
        last_reload = datetime.now()
        
        
META_TYPE = ( 
    ('description', u'description'), 
    ('keywords', u'keywords')
)
  
class Page(models.Model):
    updated = models.DateTimeField(_(u'Datum a čas poslední úpravy'), auto_now=True)
    parent = models.ForeignKey('Page',verbose_name = _(u'Nadřazená stránka'), null=True, blank=True)
    title = PageTitleField(_(u'Název'), max_length=255)
    relative_url = PageUrlField(_(u'URL'), max_length=100, blank=True, null=True)
    default = models.BooleanField(_(u'Hlavní strana'), default=False)
    order = models.IntegerField(_(u'Pořadí'), null=True, blank=True, help_text=_(u'V případě, že chcete zobrazit stránku v menu, nastavte pořadí'))
    page_type = models.CharField(_(u'Typ'), max_length=250, choices=list(get_dynamic_url_choices()))
    
    content = models.ForeignKey('PageContent',verbose_name = _(u'Obsah stránky'), null=True, blank=True)
    meta_data = models.ManyToManyField('Meta',verbose_name = _(u'Metadata'), null=True, blank=True)
    html_title = models.CharField(_(u'Titulek stránky'), max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return self.title;
    
    def _parent_url(self):
        if (self.parent):
            return self.parent.url
        return ''
    parent_url = property(_parent_url)
        
    def _url(self):
        if (self.page_type_name == 'static'):
            return '/'+self.absolute_url
        if (self.page_type_name == 'redirects'):
            for qs in (Page.objects.filter(parent = self, order__isnull = False).order_by('order'), Page.objects.filter(parent = self, order__isnull = True)):
                for page in qs:
                    if (page.is_active() and page.is_in_menu()):
                        return page.url
        if (self.page_type_name == 'redirectstourl'):
            return self.content.cast().url
        if (self.page_type_name == 'redirectstopage'):
            return self.content.cast().page.url
        from templatetags.page_utils import dynamic_reverse 
        return dynamic_reverse(self.page_type_name)
    url = property(_url)
     
    def _absolute_url(self):
        if (self.parent):
            if not self.relative_url:
                return self.parent.absolute_url
            return self.parent.absolute_url+'/'+self.relative_url

        return self.relative_url
    
    absolute_url = property(_absolute_url)

    def pattern(self):
        dynamic_url = get_dynamic_url_by_choice(self.page_type)
        if (self.page_type_name != 'redirects'):
            return dynamic_url.get_url_patterns(self)
        return None
        
    def _page_type_name(self):
        return self.page_type.split('-')[1]
    
    page_type_name = property(_page_type_name)
            
    def save(self):
        url = get_dynamic_url_by_choice(self.page_type)
        if (not url.can_be_in_menu()):
            self.default = False
            self.order = None
        
        if(self.default):
            for page in Page.objects.filter(default=True):
                page.default = False
                super(Page, page).save()
            
        
        if (self.order == None): 
            super(Page, self).save()
        else:
            pages = Page.objects.filter(order__gte = self.order, parent = self.parent).order_by('order')
            first = True
            for page in pages:
                if (first and page.order != self.order):
                    break
                page.order += 1
                page.save()
                first = False
            super(Page, self).save()
        
    def delete(self):
        pages = Page.objects.filter(order__gt = self.order, parent = self.parent).order_by('order')
        for page in pages:
            page.order -= 1
            page.save()
        super(Page, self).delete()
        
    class Meta:
        verbose_name = _(u'Stránka')
        verbose_name_plural = _(u'Stránky')
    
    @staticmethod
    def get_page(path):
        path = re.sub(r'^/','', path)
        static_pages = Page.objects.exclude(page_type = 'none-redirects')
        for page in static_pages:
            dynamic_url = get_dynamic_url_by_choice(page.page_type)
            if dynamic_url.equals(page, path):
                return page
    
        return None
    
    
    
    def is_active(self):
        if (self.page_type_name != 'redirects'):
            return True
        for page in Page.objects.filter(parent = self):
            if (page.is_active()):
                return True
        return False
    
    def is_in_menu(self):
        return self.page_type.split('-')[2] == 'menu'   

        
class PageContent(models.Model):
    id = models.CharField(_(u'Id'), max_length=100, editable=False, primary_key=True)
    real_type = models.ForeignKey(ContentType, editable=False, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.real_type = self._get_real_type()
            contents = self.__class__.objects.all().order_by('-id')
            if (contents):
                model_name, id = contents[0].id.split('$')
                id = int(id) + 1
            else :
                model_name = self.__class__.__name__.lower()
                id = 0
                
            self.id = '%s$%s' % (model_name, id)
        
        super(PageContent, self).save(*args, **kwargs)
    
    @staticmethod
    def get_content(path):
        page = Page.get_page(path)
        if (page and page.content):
            try:
                return PageContent.objects.get(pk = page.content.id).cast()
            except ObjectDoesNotExist:
                pass
        return None
    
    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def __unicode__(self):
        return self.cast().__unicode__();
    
       
    class Meta:
        verbose_name = _(u'Obsah stránky')
        verbose_name_plural = _(u'Obsah stránky')


class DefaultPageContent(PageContent): 
    title = models.CharField(_(u'Nadpis'), max_length=255) 
    subtitle = models.CharField(_(u'Podnadpis'), max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return '%s - %s' % (unicode(_(u'Obsah stránky')), self.title)
    
    class Meta:
        verbose_name = _(u'Obsah stránky')
        verbose_name_plural = _(u'Obsah stránky')

   
class RedirectToURLPageContent(PageContent):  
    url = models.URLField(_(u'URL adresa'), verify_exists=False)

    def __unicode__(self):
        return '%s - %s' % (unicode(_(u'Přesměrování na URL')), self.url);

class RedirectToPagePageContent(PageContent):
    page = models.ForeignKey(Page, verbose_name = _(u'Stránka'))
    
    def __unicode__(self):
        return '%s - %s' % (unicode(_(u'Přesměrování na stránku')), self.page);
          
class StaticPageContent(DefaultPageContent):
    html = HtmlField(_(u'Html'), blank=True)   
   
    def __unicode__(self):
        return '%s - %s' % (unicode(_(u'Statická stránka')), self.title);
    
    class Meta:
        verbose_name = _(u'Statický obsah')
        verbose_name_plural = _(u'Statický obsah')
        
        
class Meta(models.Model):
    name = models.CharField(_(u'Název'), max_length=50, choices=META_TYPE, default="description") 
    content = models.CharField(_(u'Text'), max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return '%s = %s' % (self.name, self.content);
       
    class Meta:
        verbose_name = _(u'HTML Meta tag')
        verbose_name_plural = _(u'HTML Meta tag')
        

class DynamicMeta(object):
    def __init__(self, name, content):
        self.name = name
        self.content = content
