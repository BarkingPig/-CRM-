
from django.utils.translation import ugettext as _
from django.forms import forms,ModelForm
from django.forms import ValidationError

# from crm import models
# ？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？

# 生成MODEL FORM 用于修改数据库中的记录中的数据
# class CustomerModelForm(ModelForm):
#     class Meta:
#         model =  models.Customer
#         fields = "__all__"


def create_model_form(request, admin_class):
    '''
    动态生成MODEL FORM  所有的form默认加一个clean验证
    :param request:
    :param admin_class: 相应表要显示的定制化表对象的类的对象
    :return:
    '''

    def default_clean(self):  # self是动态生成的form（model_form_class）  要在form提交后才会执行这个函数
        '''给所有的form默认加一个clean验证  验证是不是按要求修改的比较修改后的和修改前的表单form数据'''
        print("---对应的表类", admin_class)
        print("---对应的表类自定义的表单验证", admin_class.readonly_fields)
        print("---动态生成的form表单里的相应的内容（修改前的form内容）", self.instance.id)
        error_list = []  # 用来储存错误
        for field in admin_class.readonly_fields:  # 循环自定义的表单验证（只读）
            before_form_field = hasattr(self.instance,field)  # 获取修改前表单里设了自定义验证（只读）的字段
            after_form_field = self.cleaned_data.get(field)   # 获取修改后（当前）表单里设了自定义验证（只读）的字段
            if before_form_field != after_form_field:
                error_list.append(ValidationError(   # 用列表储存多个错误后同时返回（达到同时报多个错误的目的）
                    _('%(field)s 是只读字段不可以修改, 其值为%(val)s'),
                    code='invalid',
                    params={'field': field, 'val': before_form_field},
                ))

        if error_list:  # 如果有错误就返回报错
            raise ValidationError(error_list)
    def __new__(cls, *args, **kwargs):  # 更改form表单里的标签和添加标签
        #  __new__ 需要有3个参数
        # super(CustomerForm, self).__new__(*args, **kwargs)
        # print("base fields",cls.base_fields)
        for field_name, field_obj in cls.base_fields.items():  # 循环form里的标签
            # print('-------',field_name,dir(field_obj))
            if field_name in admin_class.readonly_fields:  # 在king_admin的只读列表里
                field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        # admin_class.model相对应的表对象
        fields = "__all__"

    attrs = {'Meta': Meta}
    model_form_class = type("DynamicModelForm", (ModelForm,), attrs)
    setattr(model_form_class, '__new__', __new__)
    setattr(model_form_class, 'clean', default_clean)  # 要在form提交后才会执行这个函数

    return model_form_class
