from django.contrib import admin
from crm import models
from django.shortcuts import render


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'qq','name', 'source', 'consultant', 'content',  'date')
    #  在页面显示的字段
    list_filter = ('source', 'consultant', 'date')
    # 用于筛选的字段
    search_fields = ('qq', 'name', )
    # 用于搜索的字段范围
    # raw_id_fields = ('consult_course',)
    filter_horizontal = ['tags',]
    # 显示可选的双框
    list_per_page = 1
    readonly_fields = ['qq',]

    actions = ["test_action", ]   # 对GO进行私人订制
    def test_action(self,request,record_list):
        """
         # 对GO进行私人订制
        :param request:
        :param record_list: 选中的记录组成的列表
        :return:
        """
        print('test action:',self,"---",request,'-----',record_list)
        return render(request, "king_admin/king_admin.html")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Course)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Branch)
admin.site.register(models.Enrollment)
admin.site.register(models.ClassList)
admin.site.register(models.Tag)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudentRecord)
admin.site.register(models.Payment)
admin.site.register(models.Menu)
