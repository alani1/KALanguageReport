from django import template

register = template.Library()

@register.filter(name='ftime')    
def ftime(b):
    import math

    hours = int(math.floor(b/3600))
    min  = int(math.floor(b / 60) - (hours * 60))
    secs = int(b % 60)
    
    return "{0:02d}:{1:02d}:{2:02d}".format(hours,min,secs)
    