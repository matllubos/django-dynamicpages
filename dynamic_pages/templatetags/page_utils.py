# coding: utf-8
from django import template
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode

from dynamic_pages.dynamic.utils import get_dynamic_url
from dynamic_pages.utils import quote
from dynamic_pages.models import Page #@UnresolvedImport

register = template.Library()

@register.simple_tag
def is_active(link, req_path):
    current = Page.get_page(req_path)
    while(current != None):
        if (current == link):
            return "active"
        current = current.parent
    return "no-active"
    
def mainmenu(path):
    pages = Page.objects.filter(parent__isnull = True, order__isnull = False).order_by('order')
    for page in pages:
        if (not page.is_active()):
            pages = pages.exclude(pk = page.id)
    return {'pages': pages, 'path': path}
register.inclusion_tag('pages/menu/mainmenu.html')(mainmenu) 

def footmenu(path):
    pages = Page.objects.filter(parent__isnull = True, order__isnull = False).order_by('order')
    for page in pages:
        if (not page.is_active()):
            pages = pages.exclude(pk = page.id)
    return {'pages': pages, 'path': path}
register.inclusion_tag('pages/menu/footmenu.html')(footmenu) 


def submenu(path):
    parent = Page.get_page(path)
    if (parent):
        while(parent.parent != None):
            parent = parent.parent
        pages = Page.objects.filter(parent = parent, order__isnull = False).order_by('order')
        for page in pages:
            if (not page.is_active()):
                pages = pages.exclude(pk = page.id)
        return {'pages': pages, 'path': path}
    else:
        return
register.inclusion_tag('pages/menu/submenu.html')(submenu) 

def subsubmenu(context, path, form = None):
    if not form and context.has_key('form'):
        form = context['form']
    parent = Page.get_page(path)
    if (parent and parent.parent):
        while(parent.parent.parent != None):
            parent = parent.parent
        pages = Page.objects.filter(parent = parent, order__isnull = False).order_by('order')
        for page in pages:
            if (not page.is_active()):
                pages = pages.exclude(pk = page.id)
        return {'pages': pages, 'path': path, 'form': form, 'STATIC_URL': context['STATIC_URL']}
    else:
        return {'form': form, 'STATIC_URL': context['STATIC_URL']}
register.inclusion_tag('pages/menu/subsubmenu.html', takes_context=True)(subsubmenu) 

@register.simple_tag
def title(path, dynamic_title = ''):
    page = Page.get_page(path)
    if (page == None): return dynamic_title;
    
    title = page.title
    if (page.html_title != '' and page.html_title != None): title = page.html_title
    
    if (dynamic_title):
        return '%s - %s' % (title, dynamic_title)
    return title

def meta(path, meta = []):
    page = Page.get_page(path)
    if (page == None): return {'meta_tags': None}
    meta_tags = list(page.meta_data.all())
    meta_tags += meta
    return {'meta_tags': meta_tags}
register.inclusion_tag('pages/meta.html')(meta) 

@register.filter
def url_quote(value):
    return quote(value.encode("utf-8"))

import re


def dynamic_reverse(view_name, *args):
    url = get_dynamic_url(view_name)
    if not url:
        return ''
    
    pages = Page.objects.filter(page_type = url.get_full_name())
    if not pages:
        return ''
     
    page = pages[0]
    for pattern in url.get_patterns(page):
        if (not re.search('\(.*[\?\|\+\.\*\[\]]+.*\)', pattern)):
            pattern = re.sub(r'[\)\(]', '', pattern)
        
        if (re.search(r"((\([^\)]*\)[^\)\(]*)){%s}" % len(args), pattern)):
            reverse = ''
            
            for arg in args:
                pattern = re.sub('(\([^)]*\))', smart_unicode(arg), pattern, count=1)
            
            pattern = re.sub('[\?\^\$]', '', pattern) 
            if pattern == '/':
                return pattern
            return '/%s' % pattern 
        
    return ''
    
class DynamicReverseNode(template.Node):
    '''
    Dynamic alternative to django ReverseNode
    '''
    
    def __init__(self, view_name, args):
        self.view_name = str(view_name)
        self.args = args

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        return dynamic_reverse(self.view_name, *args)
    
@register.tag
def dynamicurl(parser, token):
    content = token.split_contents()
    args = []
    for arg in content:
        try:
            args.append(parser.compile_filter(arg))
        except:
            pass
    return DynamicReverseNode(args[1], args[2:])

class QueryNode(template.Node):
    '''
    Helps with updating and changing URL queryes in templates
    '''
    
    def __init__(self, data):
        self.data = data

    def render(self, context):
        params = context['request'].GET.copy()
        for del_params in self.data['remove']:
            if params.has_key(del_params):
                del params[del_params]
        
        for key, value in self.data['new_params'].items():
            params[key] = value.resolve(context)
        return params.urlencode()
    
@register.tag
def get_query_string(parser, token):
    content = token.split_contents()
    args = {
        'new_params': {},
        'remove': []    
        }
    for arg in content[1:]:
        type, values = arg.split(':')
        for value in values.split(','):
            try:
                if type == 'new_params':
                    param = value.split('=')
                    args[type][param[0]] = parser.compile_filter(param[1])
                elif type == 'remove':
                    args[type].append(value)
            except:
                pass

    return QueryNode(args)
