This project is not CMS system but simplify developers create dynamic pages with possibility changing URL without restarting the web server. The URL can user change from the django administration. 

Each page has assigned type and page content. Standard page contents are static page, redirect to another page, redirect to url and page content which containt only title. Each page content will be available as a page_content variable in the template. It is possible adds custom page content.

Features:
========

	* Create pages which URL is possible dynamically change
	* Set page content to pages
	* Static, redirect, redirect to page, default page content
	* Custom page content
	* Dynamic reverse that return URL string from page name
	* Automatic URLs reload for every process which processes request when pages is changed
	* Tree structured admin for pages
	* Automatic admin registration of page content



Installation:
============

easy_install/pip
----------------

Firstly install djagno-simple-utilities::
	pip install -U django-simple-utilities
	easy_install django-simple-utilities
	
And finally install django-dynamic-pages::
	pip install -U django-dynamic-pages
	easy_install -U django-dynamic-pages



Configuration:
=================

settings.py:
-----------

Add utilities and dynamic_pages to INSTALLED_APPS in settings.py before django.contrib.admin::

	INSTALLED_APPS = (
 	  	 …
	   	'utilities',
	    'dynamic_pages',
		'django.contrib.admin',
   		 …
	)

add 'dynamic_pages.middleware.UrlsReloadMiddleware' to MIDDLEWARE_CLASSES and 'dynamic_pages.context_processors.page_content' into TEMPLATE_CONTEXT_PROCESSORS


urls.py:
-------
	
Firstly you must add dnamic_patterns to django patterns::

	from dynamic_pages.dynamic.utils import dynamic_urlpatterns
	urlpatterns += dynamic_urlpatterns()

After that you can set dynamic_patterns, for example::

	from dynamic_pages.dynamic.dynamic_urls import DynamicUrl
	dynamic_patterns = (
    		DynamicUrl('static', _(u'Static page'),  StaticView.as_view(), (r'',), 'dynamic_pages.StaticPageContent'),
    		DynamicUrl('redirects', _(u'Redirect to first child page')),
    		DynamicUrl('redirectstourl', _(u'Redirect to URL'), None, None, 'dynamic_pages.RedirectToURLPageContent', can_change_url = False),
    		DynamicUrl('redirectstopage', _(u'Redirect to page'), None, None, 'dynamic_pages.RedirectToPagePageContent', can_change_url = False),
	)


class dynamic url has this constructor:
	DynamicUrl(name, verbose_name, view = None, patterns = [], model = None, can_change_url = True, view_kwargs = None)
	
		* name - unique name of dynamic_pattern
		* verbose_name - name which is used in administration
		* view - django class view or string path to function
		* patterns - url patterns. Every pattern can be changed in administration, but url which is set in administration create prefix all this paterns. If you can edit the entire url in the administration set patterns to ['']
		* model - you can create custom PageContent, this model must extend PageContent model. Page content is available in template as page_content variable. This value must be string which contains app_name.model_name
		* can_change_url - is this value is set to False, you will not be able change url dynamically.
		* view_kwargs - same value as url view_kwargs


Custom page content:
--------------------

PageContent is model which contains webpage data. Every page can have one page content. You can create custom page content in your apps in model.py file. For example::

	class HomePageContent(PageContent):
    		html = HtmlField(_(u'Text'), blank=True)   
   
   		def __unicode__(self):
        		return '%s' % force_unicode(_(u'Home page content'));
    
    		class Meta:
        		verbose_name = _(u'Home page content')
        		verbose_name_plural = _(u'Home page content') 

and when you set model in right DynamicUrl as path to this model class, page_content variable will contain this page content in template.



page_utils:
-----------

page_utils contains template tags. You can use it in your templates.

{% load page_utils %}

	* dynamicurl:
		because template tag url is not working on dynamic pages, you can use tag dynamicurl::

			{% dynamicurl dynamic_pattern_name val1 val2 … %}

	* get_query_string::
		this tag help with change query strings::
			{% get_query_string remove:a,b new_params:c=5,d='e' %} - return query string which from queries removes queries a and b and adds queries c and d with values 5 and 'e'
			

TODO: In the future will be add navigation and page menu template tags.
