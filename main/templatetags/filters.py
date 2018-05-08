import django, base64
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# Text's splitter into two equal parts
def splitword(w):
    split = -((-len(w))//2)
    return w[:split], w[split:]

# Smart filter
@register.filter
@stringfilter
def truncatesmart(value):
    """
    Truncates a strings
    """

    # Asign every indexed part of text into first and second parts
    first_part, second_part = splitword(value)

    data = {}
    data['first'] = first_part # first part of string
    data['second'] = second_part # second part of string
    return data

@register.filter
def strip_language(value):
    return value.replace('/'+django.utils.translation.get_language()+'/','')