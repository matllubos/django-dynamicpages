from django.contrib.admin.filterspecs import ChoicesFilterSpec, FilterSpec,\
    RelatedFilterSpec
from django.utils.encoding import smart_unicode
from django.conf import settings


class PageSiteFilter(RelatedFilterSpec):

    def choices(self, cl):
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        for pk_val, val in self.lookup_choices:
            yield {'selected': self.lookup_val == smart_unicode(pk_val),
                   'query_string': cl.get_query_string(
                                   {self.lookup_kwarg: pk_val},
                                   [self.lookup_kwarg_isnull]),
                   'display': val}

FilterSpec.filter_specs.insert(0, (lambda f: hasattr(f, 'page_site_filter'), PageSiteFilter))
    
    