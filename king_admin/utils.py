# __author:  Administrator
# date:  2017/1/5
from django.db.models import Q

def table_filter(request, admin_class):
    '''
    进行条件过滤并返回过滤后的数据
    admin_class 要显示的字段 '''
    filter_conditions = {}  # 存筛选的键值对
    all_key_value = {}  # 前端页面的所有键值对 筛选条件 页码 排序
    for k, v in request.GET.items():
        # request.GET.items() 获取页面里的所有键值对 可能是（page = 页码，跳页时）（当 筛选出时 'source': ['1'] ）（排序的o = '-id'）
        keyword_list = ['page', 'o', 'q']  # 页面中的键值对，不是筛选字段的关键字，所以不存到filter_conditions = {}中
        if k not in keyword_list:
            if v:
                filter_conditions[k] = v
                all_key_value[k] = v
        else:
            if v:
                all_key_value[k] = v
    return admin_class.model.objects.filter(**filter_conditions), filter_conditions, all_key_value


#  admin_class.model 是 king_admin 里的 models_class: 相应的表对象 models.UserProfile


def table_order(request, object_list):
    """
    # 给数据排序
    :param request: order_key = request.GET.get('o') 获取前端页面上的排序键值对
    :param object_list: 从数据库拿到要排序的数据
    :return: object_list,排好序的数据 order_key 变了号的传给前端的下一次排序要传回来的排序键值对
    """
    order_key = request.GET.get('o')
    if order_key:  # 判断order_key是否为空，没有点击过字段名进行排序时）在页面里 O =‘’ 是不存在的
        object_list = object_list.order_by(order_key)  # 当order_key不为空那就是点了排序（order_key中有'-'为倒序没有是正序）
        if order_key.startswith('-'):  # 判断order_key中的第一个字符是不是'-'
            order_key = order_key.strip('-')  # 去掉order_key中的'-'在传回页面中,让下次点击字段排序时是相反的排法
        else:
            order_key = "-%s" % order_key  # 没有'-'就加
    return object_list, order_key

def table_search(request, admin_class, object_list):
    """

    :param request: order_key = request.GET.get('q') 获取前端页面上的搜索键值对
    :param admin_class: 是models_class: 相应的表对象 models.UserProfile
    :param object_list: 筛选后的数据
    :return:
    """
    search_value = request.GET.get('q', '')
    # 获取搜索框的值，也是以键值对的形式 这个'',是让search_value不为空
    q_obj = Q()  # q联合查询
    q_obj.connector = 'OR'
    for column in admin_class.search_fields: # 可以搜索的字段范围
        q_obj.children.append(("%s__contains" % column, search_value))  # __contains包含的都找出来
    object_list = object_list.filter(q_obj)
    print(type(object_list),'11111111111111111111111111111111111111111111111')
    return object_list

