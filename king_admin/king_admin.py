from crm import models
from django.shortcuts import render

enabled_admins = {}  # {app_name：{table_name：该表要在前端显示的字段表对象,....}}保存 数据


class BaseAdmin(object):  # 基类  前端要展示的 register()中的admin_class
    list_display = []  # 展示
    list_filter = []  # 筛选
    search_fields = []  # 搜索的字段范围
    list_per_page = 20  # 默认一页显示多少条数据
    actions = []  # 自定义执行（框）的函数
    readonly_fields = []  # 只读的表单自定义验证

class CustomerAdmin(BaseAdmin):  # 前端要展示的  register()中的admin_class
    list_display = ['id', 'qq', 'name', 'source', 'consult_course', 'date']
    list_filters = ['source', 'consultant', 'consult_course', 'date']
    search_fields = ['qq', 'name', ]
    list_per_page = 3
    actions = ["test_action", "delete_action"]  # 对GO进行私人订制
    readonly_fields = ['qq', ]

    def test_action(self, request, selected_objs):  # (views)action_func(admin_class, request, selected_objs)
        """
         # 对GO进行私人订制
        :param request:
        :param selected_objs: 选中的记录组成的列表
        :return:
        """
        print('test action:', self, "---", request, '-----', selected_objs)
        return render(request, "king_admin/king_admin.html")
    test_action.verbose_name = "测试"

    def delete_action(self, request, selected_objs):
        """
         # 对GO进行私人订制
        :param request:
        :param selected_objs: 选中的记录组成的列表
        :return:
        """
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        print("--->delete_selected_objs", self, request, selected_objs)
        if request.POST.get("delete_confirm") == "yes":
            selected_objs.delete()
            return selected_objs("/king_admin/%s/%s/" % (app_name, table_name))
        selected_ids = ','.join([str(i.id) for i in selected_objs])
        return render(request, "king_admin/record_delete.html", {"obj_list": selected_objs,
                                                                 "admin_class": self,
                                                                 "app_name": app_name,
                                                                 "table_name": table_name,
                                                                 "selected_ids": selected_ids,
                                                                 "action": request._admin_action
                                                                 })
    delete_action.verbose_name = "删除"


class TagAdmin(BaseAdmin):
    list_display = ['id', 'name']


class UserProfileAdmin(BaseAdmin):  # 前端要展示的
    list_display = ['name', ]
    list_per_page = 1


def register(models_class, admin_class=None):
    """
    取得相应的表对象，并以{app_name：{table_name：该表要在前端显示的字段表对象,....}}保存
    :param models_class: 相应的表对象 models.UserProfile
    :param admin_class:  该表要显示的定制化表对象
    :return:
    """
    if models_class._meta.app_label not in enabled_admins: #？？？？？  # models.UserProfile._meta.
        enabled_admins[models_class._meta.app_label] = {}  # 获取app name

    admin_class.model = models_class
    # 给admin_class 加一个属性 与models.class 关联起来  models_class: 相应的表对象 models.UserProfile
    enabled_admins[models_class._meta.app_label][models_class._meta.model_name] = admin_class


register(models.UserProfile, UserProfileAdmin)
register(models.Customer, CustomerAdmin)
register(models.Tag, TagAdmin)
