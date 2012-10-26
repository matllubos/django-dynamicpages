# coding: utf-8
from dynamic_pages.views import StaticView
from dynamic_pages.dynamic.dynamic_urls import DynamicUrl
from django.utils.translation import ugettext_lazy as _
from django.views.generic.simple import redirect_to

DEFAULT_DYNAMIC_URLS = (
    DynamicUrl('static', _(u'Static page'),  StaticView.as_view(), (r'',), 'dynamic_pages.StaticPageContent'),
    DynamicUrl('linktofirstpage', _(u'Link to first child page'), can_be_in_menu=True),
    DynamicUrl('linktourl', _(u'Link to URL'), None, None, 'dynamic_pages.URLPageContent', can_change_url = False, can_be_in_menu=True),
    DynamicUrl('linktopage', _(u'Link to page'), None, None, 'dynamic_pages.PagelinkPageContent', can_change_url = False, can_be_in_menu=True),
    DynamicUrl('redirecttourl', _(u'Redirect to URL'), 'dynamic_pages.views.redirect_to_url', (r'',), 'dynamic_pages.URLPageContent', can_be_in_menu=False),
    DynamicUrl('redirecttopage', _(u'Redirect to page'), 'dynamic_pages.views.redirect_to_page', (r'',), 'dynamic_pages.PagelinkPageContent', can_be_in_menu=False),
)
