from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import table_filter, table_order, table_search
from king_admin import king_admin


def king_admin_index(request):
    # print(king_admin.enabled_admin)
    return render(request, 'king_admin/king_admin.html', {'table_list': king_admin.enabled_admins})
    # 把king_admin中的全局字典传的前端，在自定义标签的模块里进行获取数据


def table_index(request, app_name, table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]  # 是models_class: 相应的表对象 models.UserProfile
    object_list, filter_conditions, all_key_value = table_filter(request, admin_class)  # 在数据库中取数据并筛选
    # filter_conditions是request.GET.items() 获取页面里的筛选的键值对
    # 是object_list储存数据的列表(还没执行)admin_class.model.objects.filter(**filter_conditions)
    # all_key_value 前端页面的所有键值对 筛选条件 页码 排序

    object_list = table_search(request, admin_class, object_list)  # 搜索

    object_list, order_key = table_order(request, object_list) # 排序
    # 给取得的数据排序重新赋给object_list，order_key是返回前端在从前端传回后端判断用哪个字段排序，是正序还是倒序
    paginator = Paginator(object_list, admin_class.list_per_page)   #  分页
    # 数据库中的总条数，和每页显示多少条，
    page = request.GET.get('page')
    # 从前端获取当前码数 page
    try:
        query_sets = paginator.page(page)
        # 根据索引number（页码 page），返回一个’Page’对象，如果不存在，引起
        # InvalidPage异常
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
        # 当页面不存在或者无效时，会引起
        # ``InvalidPage``
        # 异常，一般这个异常就够用，如果需要更
        # 详细信息，还有
        # ``PageNotAnInteger``，``EmptyPage``
        # filter_conditions,GET.items() 获取页面里的键值对组成的字段 可能是（page = 页码，跳页时）
    return render(request, "king_admin/table.html", {"admin_class": admin_class,  # 是models_class: 相应的表对象 models.UserProfile
                                                     "query_sets": query_sets,  # 根据索引number（页码 page），返回一个’Page’对象，
                                                     "filter_conditions": filter_conditions,   # filter_conditions存有筛选的筛选条件（以键值对的形式）
                                                     "all_key_value": all_key_value,  # 前端页面的所有键值对 筛选条件 页码 排序
                                                     "order_key": order_key})  # order_key是返回前端在从前端传回后端判断用哪个字段排序，是正序还是倒序

