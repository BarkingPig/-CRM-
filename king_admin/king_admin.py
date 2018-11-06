from crm import models
from django.shortcuts import render
from django.forms import ValidationError  # form验证的报错模块
from django.utils.translation import ugettext as _  # 国际化模块

enabled_admins = {}  # {app_name：{table_name：该表要在前端显示的字段表对象,....}}保存 数据


class BaseAdmin(object):  # 基类  前端要展示的 register()中的admin_class
    list_display = []  # 展示
    list_filter = []  # 筛选
    search_fields = []  # 搜索的字段范围
    list_per_page = 20  # 默认一页显示多少条数据
    actions = []  # 自定义执行（框）的函数
    readonly_fields = []  # 只读的表单自定义验证

    def delete_record_action(self, request, selected_objs):
        """
         # 对GO进行私人订制  删除选中记录
        :param request:
        :param selected_objs: 选中的记录组成的列表
        :return:
        """
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        # print("--->delete_selected_objs", self, request, selected_objs)
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

    delete_record_action.verbose_name = "删除"

    def default_form_verification(self):
        """
        用户可以在此进行自定义的表单验证，相当于django form的clean方法
        可以进行多个验证
        用户自定义的（默认的表单验证）
        :return:
        """
        pass


class StudentAdmin(BaseAdmin):  # 前端要展示的  register()中的admin_class
    list_display = ['id', 'name']
    list_filters = ['dorm', 'name']
    search_fields = ['id', 'name', ]
    list_per_page = 3
    # actions = ["test_action", "delete_record_action"]  # 对GO进行私人订制
    # readonly_fields = ['qq',]
    #
    #
    # def test_action(self, request, selected_objs):  # (views)action_func(admin_class, request, selected_objs)
    #     """
    #      # 对GO进行私人订制
    #     :param request:
    #     :param selected_objs: 选中的记录组成的列表
    #     :return:
    #     """
    #     print('test action:', self, "---", request, '-----', selected_objs)
    #     return render(request, "king_admin/king_admin.html")
    # test_action.verbose_name = "测试"

# def default_form_verification(self):
#     """
#     这个self是动态生成的form（model_form_class)有数据的那种
#     用户可以在此进行自定义的表单字段验证，相当于django form的clean方法
#     用户自定义的（默认的表单验证）
#     验证是不是按要求修改的比较修改后的和修改前的表单form数据
#     :return:
#     """
#     extra_error_list = []
#     content_restrict = self.cleaned_data['content']
#     if len(content_restrict) > 15:
#         extra_error_list.append(ValidationError(  # 用列表储存多个错误后同时返回（达到同时报多个错误的目的）
#             _('%(field)s 字数不可以超过15个，恭喜你已经成功超过15个！！！！'),
#             code='invalid',
#             params={'field': 'content',},
#         ))
#
#     return extra_error_list

# def clean_name(self):
#     """
#     form表单中单个字段的自定义
#     :return:
#     """
#     # print("name clean validation:", self.cleaned_data["name"])
#     if not self.cleaned_data["name"]:
#         self.add_error('name', "不可以为空")



class UserProfileAdmin(BaseAdmin):  # 前端要展示的
    list_display = ['name', ]
    readonly_fields = ['password', ]
    list_per_page = 1

class ClassListAdmin(BaseAdmin):
    list_display = ['id', 'name']
    list_filters = ['id', 'name']
    search_fields = ['id', 'name', ]
    list_per_page = 3

class DormAdmin(BaseAdmin):
    list_display = ['id', 'name','address']
    list_filters = ['id', 'name']
    search_fields = ['id', 'name', ]
    list_per_page = 8

def register(models_class, admin_class=None):
    """
    取得相应的表对象，并以{app_name：{table_name：该表要在前端显示的字段表对象,....}}保存
    :param models_class: 相应的表对象 models.UserProfile
    :param admin_class:  该表要显示的定制化表对象
    :return:
    """
    if models_class._meta.app_label not in enabled_admins:  # ？？？？？  # models.UserProfile._meta.
        enabled_admins[models_class._meta.app_label] = {}  # 获取app name

    admin_class.model = models_class
    # 给admin_class 加一个属性 与models.class 关联起来  models_class: 相应的表对象 models.UserProfile
    enabled_admins[models_class._meta.app_label][models_class._meta.model_name] = admin_class


register(models.UserProfile, UserProfileAdmin)

register(models.Student, StudentAdmin)

register(models.ClassList, ClassListAdmin)

register(models.Dorm, DormAdmin)
