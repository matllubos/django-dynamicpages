# coding: utf-8
from django import forms
from django.utils.translation import ugettext as _

from dynamic_pages.models import Page #@UnresolvedImport
from dynamic_pages.dynamic.utils import get_dynamic_url_by_choice #@UnresolvedImport

class PageForm(forms.ModelForm):
    '''
    Dynamic page validation form
    '''
    
    def clean(self):
        cleaned_data = super(PageForm, self).clean()

        page_type = cleaned_data.get("page_type")
        if not self.instance.pk and (not (page_type in 'staticpagecontent-static-menu', 'redirecttourlpagecontent-redirectstourl-menu')) and Page.objects.filter(page_type = page_type):
            self._errors["page_type"] = self.error_class([_(u'Page with this type already exists')])
            

        content = cleaned_data.get("content")
        url = get_dynamic_url_by_choice(page_type)
        if (url.has_model()):
            if (not content):
                self._errors["content"] = self.error_class([_(u'Page content cannot be empty')])
            elif (url.get_model_name() != '%s.%s' % (content.cast()._meta.app_label, content.cast()._meta.object_name.lower())):
                self._errors["content"] = self.error_class([_(u'Wrong page content')])
        else:
            if (content):
                cleaned_data["content"] = None

        return cleaned_data
    
    class Meta:
        model = Page
