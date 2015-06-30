from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def include_string(context, string):
    return template.Template(string).render(context)

@register.simple_tag(takes_context=True)
def include_docstring(context, obj):
    return template.Template(obj.__doc__).render(context)
