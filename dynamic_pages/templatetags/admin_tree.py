from django import template
from django.contrib.admin.templatetags.admin_list import result_hidden_fields, result_headers, results
from django.utils.safestring import mark_safe

from dynamic_pages.models import Page #@UnresolvedImport

register = template.Library()

def tree_result_headers(cl):
    tree_result_headers = list(result_headers(cl))
    tree_result_headers.insert(1, {'text:': ''})
    return tree_result_headers
    
    
def tree_results(cl):
    tree_results = list(results(cl))
    
    sorted_tree_results = []
    for id in cl.tree_sort(None):
        i = 0
        for obj in cl.get_query_set():
            if (obj.id == id):
                tree_results[i].insert(1, mark_safe(u'<td style="padding: 0 0 0 %spx; width: 50px;">|-</td>' % (cl.get_depth(obj) * 20 + 20)))
                sorted_tree_results.append(tree_results[i])
            i += 1

    return sorted_tree_results


def result_tree(cl):
    """
    Displays the headers and data list together
    """
    tree_results(cl)    
    tree_result_headers(cl)   
 
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(tree_result_headers(cl)),
            'results': list(tree_results(cl))}
result_list = register.inclusion_tag("admin/change_tree_results.html")(result_tree)