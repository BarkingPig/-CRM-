from crm import models

enabled_admin = {}  # {app_name：{table_name：该表要在前端显示的字段表对象,....}}保存 数据


class BaseAdmin(object):  # 基类  前端要展示的 register()中的admin_class
    list_display = []
    list_filter = []


class CustomerAdmin(BaseAdmin):  # 前端要展示的  register()中的admin_class
    list_display = ['qq', 'name']


class UserProfileAdmin(BaseAdmin):  # 前端要展示的
    list_display = ['name']


def register(models_class, admin_class=None):
    """
    取得相应的表对象，并以{app_name：{table_name：该表要在前端显示的字段表对象,....}}保存
    :param models_class: 相应的表对象 models.UserProfile
    :param admin_class:  要显示的字段对象
    :return:
    """
    if models_class._meta.app_label not in enabled_admin:  # models.UserProfile._meta.
        enabled_admin[models_class._meta.app_label] = {} # 获取app name

    admin_class.model = models_class  # 给admin_class 加一个属性 与models.class 关联起来
    enabled_admin[models_class._meta.app_label][models_class._meta.model_name] = admin_class


register(models.UserProfile, UserProfileAdmin)
register(models.Customer, CustomerAdmin)
