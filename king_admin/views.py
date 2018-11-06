from django.shortcuts import render,redirect

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.utils import table_filter, table_order, table_search
from king_admin import king_admin,forms



def king_admin_index(request):
    # print(king_admin.enabled_admin)
    return render(request, 'king_admin/king_admin.html', {'table_list': king_admin.enabled_admins})
    # 把king_admin中的全局字典传的前端，在自定义标签的模块里进行获取数据


def table_index(request, app_name, table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    # 是models_class: 相应的表对象 models.UserProfile

    if request.method == "POST": #action（执行） 来了，取前端选取的数据
        # print('--------------------',request.POST)
        selected_ids = request.POST.get("selected_ids")  # 取选择中的数据id
        action = request.POST.get("action")  # 取选中的操作执行函数
        if selected_ids:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids.split(','))  # 取数据
        else:
            raise KeyError("没有数据！")
        if hasattr(admin_class, action):
            action_func = getattr(admin_class, action)
            request._admin_action = action  # ？？？？？？？？？？？？？？？？
            return action_func(admin_class, request, selected_objs)  # ?????????admin_class

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
                                                     "order_key": order_key,
                                                     })  # order_key是返回前端在从前端传回后端判断用哪个字段排序，是正序还是倒序


def record_change_index(request, app_name, table_name, record_id):
    """

    :param request: 前端传的关键字等
    :param app_name: app名
    :param table_name: 表名
    :param record_id: 要修改的记录对象
    :return:
    """
    admin_class = king_admin.enabled_admins[app_name][table_name]  # 表类对象
    model_form_class = forms.create_model_form(request, admin_class)  # 动态添加form

    record_obj = admin_class.model.objects.get(id=record_id)  #  获取的记录对象
    if request.method == "POST":  # 获取前端修改的form
        form_obj = model_form_class(request.POST, instance=record_obj)  # 更新修改表单,获取表单对象
        if form_obj.is_valid():
                form_obj.save()  # 获得报错返回前端显示
    else:
        form_obj = model_form_class(instance=record_obj)  # 让form中有对应的数据
    # print("--------------------------------------11111111111",form_obj.errors.get('__all__'))
    # print("--------------------------------------",dir(form_obj['name']))
    # print("--------------------------------------",form_obj['name'].value)
    # print("--------------------------------------", dir(form_obj['name'].errors))
    # print("--------------------------------------",form_obj['name'].errors.data)

    return render(request, 'king_admin/record_change.html',{'form_obj': form_obj,
                                                            "app_name": app_name,
                                                            "table_name": table_name
                                                            })

def record_change_password_index(request, app_name, table_name, record_id):
        admin_class = king_admin.enabled_admins[app_name][table_name]
        record_obj = admin_class.model.objects.get(id=record_id)  # 获取的记录对象
        errors = {}  # 储存错误
        if request.method == 'POST':
            _password1 = request.POST.get("password1")  # 从前端取数据 get（name）
            _password2 = request.POST.get("password2")
            if _password1 == _password2:
                if len(_password1) > 5:  # 密码的长度，复杂度
                    record_obj.set_password(_password1)  # 给密码加严
                    record_obj.save()  # 把更改的密码就存到数据库中
                    return redirect(request.path.rsplit('password/'))   # url 去password/
                else:
                    errors['新密码不安全'] = '大于5个字符。。。。。。'
            else:
                errors['两次输入不一致'] = '请输入相同的密码'
        return render(request, 'king_admin/record_change_password.html', {'record_obj': record_obj,
                                                                          'errors': errors
                                                                          })


def record_add_index(request, app_name, table_name):
    """

    :param request: 前端传的关键字等
    :param app_name: app名
    :param table_name: 表名
    :return:
    """
    admin_class = king_admin.enabled_admins[app_name][table_name]
    admin_class.is_add_form = True  # ??????????
    model_form_class = forms.create_model_form(request, admin_class)
    print('8888888888888888888888888888888888',model_form_class)
    if request.method == "POST":
        form_obj = model_form_class(request.POST)  # 给出空表单 ？？？？？？？？？？？？？？？？？？
        print(form_obj)
        if form_obj.is_valid():
            print('00000000000000000000000000000000000000000000',form_obj.is_valid())
            form_obj.save()  # 把表单储存到数据库中
            return redirect(request.path.replace("/add/", "/"))  # ?????????
    else:
        form_obj = model_form_class()  # 空表单

    return render(request, 'king_admin/record_add.html', {'form_obj': form_obj})


def record_delete_index(request, app_name, table_name , obj_id):
    """
    删除页面，显示删除记录产生的影响
    :param request: 前端传的关键字等
    :param app_name: app名
    :param table_name: 表名
    :param obj_list: 要删除的记录对象组成的列表（可能涉及到同时删除多个记录）
    :return:
    """
    obj_list =[]
    admin_class = king_admin.enabled_admins[app_name][table_name]

    obj_list.append(admin_class.model.objects.get(id=obj_id))

    if admin_class.readonly_table:
        errors = {"readonly_table": "table is readonly ,obj [%s] cannot be deleted" % obj_list[0]}
    else:
        errors = {}
    if request.method == "POST":
        if not admin_class.readonly_table:
            obj_list[0].delete()
            return redirect("/king_admin/%s/%s/" %(app_name,table_name))

    return render(request, 'king_admin/record_delete.html',{  "obj_list":obj_list,
                                                              "admin_class" : admin_class,
                                                              "app_name": app_name,
                                                              "table_name": table_name,
                                                              "errors": errors
                                                              })