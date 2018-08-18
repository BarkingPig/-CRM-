from django.shortcuts import render

# Create your views here.
from  king_admin import  king_admin

def king_admin_index(request):
    # print(king_admin.enabled_admin)
    return render(request, 'king_admin/king_admin.html', {'table_list':king_admin.enabled_admin})
    # 把king_admin中的全局字典传的前端，在自定义标签的模块里进行获取数据

def table_index(request):

    return render(request, 'king_admin/table.html')