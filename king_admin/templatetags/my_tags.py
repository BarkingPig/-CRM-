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
def build_table_row(request, obj, admin_class):
    '''
    生成数据内容的,填充到table中,展示前端 # 为数据的id添加跳转修改页面的链接
    :param obj: 一个’Page’对象（一个页面里所有显示的数据的对象）中的obj 单条数据对象
    :param admin_class: 需要显示的字段
    :return:
    '''
    row_ele = ''
    for index, column in enumerate(admin_class.list_display):  # enumerate获取列表的索引index
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
        if index == 0:  # 为数据的id添加跳转修改页面的链接
            row_ele += "<td><a href='{request_path}{obj_id}/change/'/>{column_data}</a></td>".format(
                request_path=request.path,
                obj_id=obj.id,
                column_data=column_data)
        else:
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
def dispose_filter_time(admin_class):
    not_list_filter = []
    list_filter = admin_class.model.list_filters
    for condition in list_filter:
        field_obj = admin_class.model._meta.get_field(condition)
        if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
            condition = condition + '__gte'
        not_list_filter.append(condition)


@register.simple_tag
def render_filter_ele(condition, admin_class, filter_conditions):
    """
    构建筛选的组件（给组件导入数据）
    :param condition: 筛选的字段
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
        today_ele = datetime.now().date()  # 今天时间
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天到现在", today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])

        selected = ''
        for item in date_els:
            if filter_conditions.get(condition + '__gte') == item[1].strftime("%Y-%m-%d"):  # str(item[1])一个时间段
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])

            selected = ''
        condition = "%s__gte" % condition  # a__gte=0 也就是找大于0的所有数据

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
def add_url_keys(admin_class, all_key_value, *not_keys):
    """
    {#关于请求方式为GET的form表单，action属性后不能带参数的问题,让关键字变成表单的传入值#}
    :param all_key_value: 原先页面所有的键值对（字典的形式）
    :param *not_keys :不需在给给表单添加的关键值（表单自身的关键字不需要再传）
    :return:
    """
    eles = ''
    if not_keys[0] == 'list':
        not_list_filter = []
        for condition in not_keys[1]:
            field_obj = admin_class.model._meta.get_field(condition)
            if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
                condition = condition + '__gte'
            not_list_filter.append(condition)
        not_keys = not_list_filter

    for k, v in all_key_value.items():
        # print(type(k), '777777777777777777777777777777777')
        if k not in not_keys and '__gte' not in k:
            ele = """<input type="hidden" name="%s" value="%s">""" % (k, v)
        else:
            ele = ''
        eles += ele

    return mark_safe(eles)


@register.simple_tag
def get_table_name(admin_class):
    """
    获取表的别名
    :param admin_class:  表的对象
    :return:
    """
    return admin_class.model._meta.verbose_name_plural


@register.simple_tag
def get_associated_record(obj_list):
    '''
    把要删除记录对象及所有相关联的记录取出来
    :param obj_list: 要删除记录对象组成的列表
    :return:
    '''
    if obj_list:
        return mark_safe(recursive_related_objs_lookup(obj_list))


def recursive_related_objs_lookup(obj_list):
    """
    列出和要删除记录对象的相关对象(递归)
    :param obj_list: 要删除的记录对象(删除多个记录时，记录对象是存于obj_list列表中)
    :return:
    """

    ul_ele = "<ul>"
    for obj in obj_list:
        li_ele = '''<li> %s: %s </li>''' % (obj._meta.verbose_name_plural, obj.__str__().strip("<>"))
        # obj._meta.verbose_name_plural 记录所在表的别名  obj.__str__().strip("<>")去<>括号
        ul_ele += li_ele

        # for local many to many
        # print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many:
            # obj._meta.local_many_to_many把所有跟这个对象直接关联的m2m表的相关联字段取出来了（多对多），
            # 可能存在多个表和该要删除记录所在表有多对多的关系
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj, m2m_field.name)  # getattr(customers中要删除的记录对象, 'tags') 得到这个对象tags字段的值
            for o in m2m_field_obj.select_related():
                # customer.tags.select_related()通过多对多外键获取删除记录的多对多的链接的表中的对应记录
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele += li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  # 最终跟最外层的ul相拼接

        for related_obj in obj._meta.related_objects:
            # 获取和obj(要删除的记录)直接相关的关联表（也就是主动联系（有ManyToManyRel的一方表记录）得不到多对多  被动链接的一方可以得到）
            if 'ManyToManyRel' in related_obj.__repr__():
                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    print("-------ManyToManyRel", accessor_obj, related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):
                        # select_related() == all() 只有ManyToManyRel有'select_related'
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele = "<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name_plural, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj, related_obj.get_accessor_name()):
                # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj, related_obj.get_accessor_name())  # ???????????????????????????
                # 上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                    target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()
                else:
                    print("one to one i guess:", accessor_obj)
                    target_objs = accessor_obj

                if len(target_objs) > 0:
                    # print("\033[31;1mdeeper layer lookup -------\033[0m")
                    # nodes = recursive_related_objs_lookup(target_objs,model_name)
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele += "</ul>"
    return ul_ele


@register.simple_tag
def get_action_verbose_name(admin_class, action):
    """
    获取自定义（执行框里的）功能（函数）的别名
    :param admin_class: king_admin里定义的表对象（自定义的执行功能函数是写在king_admin里的）是表对象下的一个函数
    :param action:
    :return:
    """
    action_func = getattr(admin_class, action)  # 获取对应的函数
    if hasattr(action_func, 'verbose_name'):  # 判断函数里是否有别名
        action_verbose_name = getattr(action_func, 'verbose_name')
    else:
        action_verbose_name = action
    return action_verbose_name
