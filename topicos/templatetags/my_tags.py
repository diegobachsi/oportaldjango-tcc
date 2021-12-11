from django import template

register = template.Library()

@register.filter
def minutos(segundos):
    return segundos / 60