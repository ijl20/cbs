from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

#############################################################
# room_app template filter for dictionary lookup            #
# use {% load ra_templatetags %}
# use with {{ mydict| ra_lookup:keyvar }}                   #
#############################################################
@register.filter
def ra_lookup(dictionary, key):
    return dictionary.get(key)
    
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)
