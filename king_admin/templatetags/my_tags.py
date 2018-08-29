# 从数据库中取数据也是在这里

from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
register = template.Library()  # register的名字是固定的,不可改变


@register.simple_tag
def app_table_name(admin_class):
    '''渲染动态获取app下的表的别名名'''
    return admin_class.model._meta.verbose_name_plural


@register.simple_tag
def build_table_row(obj, admin_class):
    '''
    生成数据内容的td,填充到table中,展示前端
    :param obj: 一个’Page’对象（一个页面里所有显示的数据的对象）
    :param admin_class: 需要显示的字段
    :return:
    '''
    row_ele = ''
    for column in admin_class.list_display:
        # 获取每个字段的类型的对象
        # print(obj, '1231231231123123123123123')
        field_obj = obj._meta.get_field(column)
        # 判断是否是choice字段
        if field_obj.choices:
            # 如果是choice字段,则按照choice的值进行展示
            column_data = getattr(obj, "get_%s_display" % column)()
        else:
            # 否则通过反射去对象中取值
            column_data = getattr(obj, column)

        if type(column_data).__name__ == 'datetime':
            # 如果是时间类型,则需要进行格式化显示
            column_data = column_data.strftime('%Y-%m-%d %H:%M:%S')
        row_ele += '<td>%s</td>' % column_data
    return mark_safe(row_ele)


@register.simple_tag
def render_page_ele(loop_counter, query_sets, all_key_value):
    """
     分页
     如果当前页数-循环的次数小于1,就展示前面两页和后面两页
     例如当前是第五页则展示3,4,5,6,7页
     :param all_key_value: # 前端页面的所有键值对 筛选条件 页码 排序
     :param loop_counter: 循环到的页码
     :param query_sets: 是 ’Page’对象

     :return:
     """
    add_key_value = filter_key_value(all_key_value, 'page')
    # 用add_key_value储存拼接筛选的筛选条件,用于在筛选后分页时点击下一页直接传到table_filter用于筛选数据
    # 用于在筛选后分页时点击下一页的内容还是筛选后的内容

    if loop_counter <= 2 or (loop_counter >= query_sets.paginator.num_pages - 1):
        # 1,2页码，最后两个页码要打印
        ele_class = ''
        if query_sets.number == loop_counter:
            ele_class = 'active'
        ele = '<li class="%s"><a href="?page=%s%s">%s</a></li>' % (ele_class, loop_counter, add_key_value, loop_counter)
        return mark_safe(ele)

    if abs(query_sets.number - loop_counter) <= 1:
        # #query_sets.number当前页
        # 当前页 减 循环到的页码的绝对值 显示当前页的前一页的页码和后一页的页码
        ele_class = ''
        if query_sets.number == loop_counter:
            ele_class = 'active'
        ele = '<li class="%s"><a href="?page=%s%s">%s</a></li>' % (ele_class, loop_counter, add_key_value, loop_counter)
        return mark_safe(ele)

    if (query_sets.number >= 4 and loop_counter == 3) or (
            query_sets.number <= query_sets.paginator.num_pages - 4 and loop_counter == query_sets.paginator.num_pages - 2):
        # 打印...
        ele = '<li class=" "><a href="#">%s</a></li>' % '...'
        return mark_safe(ele)

    return ''


@register.simple_tag
def render_filter_ele(condition, admin_class, filter_conditions):
    """
    构建筛选的组件（给组件导入数据）
    :param condition: 筛选的字段 键值对
    :param admin_class: admin_class.model models_class: 相应的表对象 models.UserProfile
    :param filter_conditions: request.GET.items() 存有筛选的筛选条件（以键值对的形式）request.GET.items()
    :return:
    """
    select_ele = '''<select class="form-control" name='{condition}' ><option value=''>----</option>'''
    # 给筛选框命名
    field_obj = admin_class.model._meta.get_field(condition)
    # 获取筛选框筛选的跳件（筛选字段的数据）
    if field_obj.choices:  # 如果筛选字段是choice类型
        selected = ''
        for choice_item in field_obj.choices:
            # print(field_obj.choices)  field_obj.choices 是集合（set）里面存着元组（tuple）
            # {(4, '51CTO'), (1, 'QQ群'), (6, '市场推广'), (3, '百度推广'), (5, '知乎'), (0, '转介绍'), (2, '官网')}
            # choice_item (4, '51CTO')
            # print("choice",choice_item,filter_conditions.get(condition),type(filter_conditions.get(condition)))
            if filter_conditions.get(condition) == str(choice_item[0]):
                # filter_conditions.get(condition) 获取页面里 筛选字段里的筛选条件
                selected = "selected"
                # option 筛选被选定的属性

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    elif type(field_obj).__name__ == "ForeignKey":  # 如果筛选字段是外键
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:  # 不从第0个开始，从1开始 0是‘-------------------’
            # print(field_obj.get_choices()[0],'ccccccccccccccccccccccccccccccccccccccccccccccc')
            if filter_conditions.get(condition) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        date_els = []
        today_ele = datetime.now().date()
        print(today_ele, today_ele - timedelta(days=7), '44444444444444444444444444444444444444444444')
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天", today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])

        selected = ''
        for item in date_els:
            if filter_conditions.get(condition) == str(item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])
            selected = ''
        condition = "%s__gte" % condition  # ????????

    select_ele += "</select>"
    select_ele = select_ele.format(condition=condition)  # 替换select_ele中的condition
    # select_ele = '''<select class="form-control" name='{condition}' ><option value=''>----</option>'''
    return mark_safe(select_ele)


@register.simple_tag
def render_order_ele(order_key, column, all_key_value):
    '''
    以字段排序
    :param order_key:  后端传回前端的下一次排序的（连续按两次同一字段排序就是一正一反排序）
    :param column: 当前循环到的字段
    :param all_key_value: 原页面的所有键值对
    :return:
    '''
    add_key_value = filter_key_value(all_key_value, 'page', 'o')
    # 用add_key_value储存拼接筛选的筛选条件,用于在筛选后分页时点击下一页直接传到table_filter用于筛选数据
    # 用于在筛选后分页时点击下一页的内容还是筛选后的内容
    if order_key:  # 变了号的传给前端的下一次排序要传回来的排序键值对
        ele_add = ''
        if order_key.startswith('-') and order_key.strip('-') == column:
            # 判断order_key中的第一个字符是不是'-' 只有排序的字段才添加排序符号
            ele_add = """ 
            <span class="glyphicon glyphicon-menu-up" aria-hidden="true">
            </span>"""  # 倒序
        elif order_key == column:
            ele_add = """ 
            <span class="glyphicon glyphicon-menu-down" aria-hidden="true">
            </span>"""
        else:
            order_key = column  # 当点击新的字段排序时，order_key = 新字段
        ele = """ <th><a href = "?o=%s%s"> %s </a>%s</th>""" % (order_key, add_key_value, column, ele_add)
    else:
        ele = """ <th><a href = "?o=%s%s"> %s </a></th>""" % (column, add_key_value, column)

    return mark_safe(ele)


@register.simple_tag
def filter_key_value(all_key_value, *needless_key_value):
    '''
    当排序，筛选，下一页时都是要更新页面的，可能在翻页时 要保存筛选的结果 排序不要原来的页码，要跳转第一页
    该函数就是让你选出你不需要的原先页面的键值对保存你要的键值对
    :param all_key_value: 原先页面所有的键值对（字典的形式）
    :param needless_key_value: 你不需要的键值对（以键的列表形式）
    :return:add_key_value 返回你需要的键值对（以添加到a标签的href的字符串形式）
    '''
    add_key_value = ''
    # print(type(all_key_value))  # 'generator' request.GET.items() 在前端循环不了
    keyword_list = needless_key_value
    for k, v in all_key_value.items():
        if k not in keyword_list:
            if v:
                add_key_value += '&%s=%s' % (k, v)
        # 用add_key_value储存拼接筛选的筛选条件,用于在筛选后分页时点击下一页直接传到table_filter用于筛选数据
        # 用于在筛选后分页时点击下一页的内容还是筛选后的内容
    return add_key_value


@register.simple_tag
def have_key_value(all_key_value, key):
    """
    获取all_key_value字典里的值
    :param all_key_value: 原先页面所有的键值对（字典的形式）
    :param key: 要获取值对应的键
    :return: value 返回的值
    """
    if key in all_key_value:  # 页面一开始有一下键不存在
        value = all_key_value[key]
    else:
        value = ''
    return value

@register.simple_tag
def add_url_keys(all_key_value, *not_keys):
    """
    {#关于请求方式为GET的form表单，action属性后不能带参数的问题,让关键字变成表单的传入值#}
    :param all_key_value: 原先页面所有的键值对（字典的形式）
    :param *not_keys :不需在给给表单添加的关键值（表单自身的关键字不需要再传）
    :return:
    """
    eles = ''
    if not_keys[0] == 'list':
        not_keys = not_keys[1]
    for k, v in all_key_value.items():
        if k not in not_keys:
            ele = """<input type="hidden" name="%s" value="%s">""" % (k, v)
        else:
            ele = ''
        eles += ele

    return mark_safe(eles)