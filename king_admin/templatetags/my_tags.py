# 从数据库中取数据也是在这里

from django import template
#from django.utils.safestring import mark_safe

register = template.Library()   #register的名字是固定的,不可改变

@register.simple_tag
def app_table_name(admin_class):
    '''渲染动态获取app下的表的别名名'''
    return admin_class.model._meta.verbose_name_plural