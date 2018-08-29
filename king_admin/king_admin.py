from crm import models

enabled_admins = {}  # {app_name：{table_name：该表要在前端显示的字段表对象,....}}保存 数据


class BaseAdmin(object):  # 基类  前端要展示的 register()中的admin_class
    list_display = []   # 展示
    list_filter = []    # 筛选
    search_fields = []
    list_per_page = 20  # 默认一页显示多少条数据


class CustomerAdmin(BaseAdmin):  # 前端要展示的  register()中的admin_class
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'consult_course', 'date']
    list_filters = ['id', 'source', 'consultant', 'consult_course', 'date']
    search_fields = ['qq', 'name', ]
    list_per_page = 1


class UserProfileAdmin(BaseAdmin):  # 前端要展示的
    list_display = ['name',]
    list_per_page = 1


def register(models_class, admin_class=None):
    """
    取得相应的表对象，并以{app_name：{table_name：该表要在前端显示的字段表对象,....}}保存
    :param models_class: 相应的表对象 models.UserProfile
    :param admin_class:  要显示的字段对象
    :return:
    """
    if models_class._meta.app_label not in enabled_admins:  # models.UserProfile._meta.
        enabled_admins[models_class._meta.app_label] = {}  # 获取app name

    admin_class.model = models_class  # 给admin_class 加一个属性 与models.class 关联起来  models_class: 相应的表对象 models.UserProfile
    enabled_admins[models_class._meta.app_label][models_class._meta.model_name] = admin_class


register(models.UserProfile, UserProfileAdmin)
register(models.Customer, CustomerAdmin)
