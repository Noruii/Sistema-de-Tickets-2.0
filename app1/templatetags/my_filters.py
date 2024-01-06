# Para agregar atributos a los forms de Django de auth_views en templates/registro/registration/
from django import template

register = template.Library()

@register.filter
def add_attr(field, css):
    attrs = {}
    definitions = css.split(',')
    for definition in definitions:
        attr, value = definition.split(':')
        attrs[attr.strip()] = value.strip()
    return field.as_widget(attrs=attrs)