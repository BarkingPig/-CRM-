from django.forms import forms,ModelForm

# from crm import models
#？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？

# 生成MODEL FORM 用于修改数据库中的记录中的数据
# class CustomerModelForm(ModelForm):
#     class Meta:
#         model =  models.Customer
#         fields = "__all__"




def create_model_form(request,admin_class):
    '''
    动态生成MODEL FORM
    :param request:
    :param admin_class: 相应表要显示的定制化表对象
    :return:
    '''

    def __new__(cls, *args, **kwargs):  # 更改form表单里的标签和添加标签
        #  __new__ 需要有3个参数
        # super(CustomerForm, self).__new__(*args, **kwargs)
        print("base fields",cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():  # 循环form里的标签
            print('-------',field_name,dir(field_obj))
            if field_name in admin_class.readonly_fields:  # 在king_admin的只读列表里
                field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        # admin_class.model相对应的表对象
        fields = "__all__"
    attrs = {'Meta':Meta}
    model_form_class =  type("DynamicModelForm",(ModelForm,),attrs)
    setattr(model_form_class,'__new__',__new__)

    return model_form_class