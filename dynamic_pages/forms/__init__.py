# coding: utf-8
from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from utilities.models.fields import TreeForeignKey

# This is not best solution, but is simplest
class PageSelect(forms.Select):
    
    def render_option(self, selected_choices, option_value, option_label):
        if option_value:
            from dynamic_pages.models import Page
            
            option_value = force_unicode(option_value)
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            return u'<option value="%s"%s class="%s">%s</option>' % (
                escape(option_value), selected_html,
                force_unicode(Page.objects.get(pk = option_value).publish_on.pk),
                conditional_escape(force_unicode(option_label)))
        return super(PageSelect, self).render_option(selected_choices, option_value, option_label)

class PageTreeForeignKey(TreeForeignKey):
    
    def formfield(self, **kwargs):
        defaults = {
            'widget': PageSelect
        }
        defaults.update(kwargs)
        return super(PageTreeForeignKey, self).formfield(**defaults)