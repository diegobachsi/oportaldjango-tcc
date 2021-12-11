import math
from django import template

register = template.Library()

@register.filter
def horas(segundos):

    if segundos >= 3600:
        hora = int(segundos/3600)
    else:
        hora = 0

    if hora < 10:
        return '0{}'.format(hora)
    else:
        return hora
       

@register.filter
def minutos(segundos):

    if segundos >= 3600:
        min = int((segundos/3600 - int(segundos/3600)) * 60)
    else:
        min = int(segundos/60)
    
    if min < 10:
        return '0{}'.format(min)
    else:
        return min


@register.filter
def segundos(segundos):

    if segundos >= 3600:
        min = (segundos/3600 - int(segundos/3600)) * 60
        seg = (min - int(min)) * 60
    else:
        min = segundos/60
        seg = (min - int(min)) * 60

    seg = math.ceil(seg)

    if seg < 10:
        return '0{}'.format(seg)
    else:
        return seg


