# coding: utf-8
from dynamic_pages.views import StaticView
from dynamic_pages.dynamic.dynamic_urls import DynamicUrl
from django.utils.translation import ugettext_lazy as _
    
DEFAULT_DYNAMIC_URLS = (
    DynamicUrl('static', _(u'Static page'),  StaticView.as_view(), (r'',), 'dynamic_pages.StaticPageContent'),
    DynamicUrl('redirects', _(u'Redirect to first child page')),
    DynamicUrl('redirectstourl', _(u'Redirect to URL'), None, None, 'dynamic_pages.RedirectToURLPageContent', can_change_url = False),
    DynamicUrl('redirectstopage', _(u'Redirect to page'), None, None, 'dynamic_pages.RedirectToPagePageContent', can_change_url = False),
)
