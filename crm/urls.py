
from crm import views
from django.urls import path

urlpatterns = [
    path('$', views.index),  # 首页
    path('salesman/', views.salesman_index, name = 'salesman_index'),
    path('customer/', views.salesman_index, name = 'customer_index'),
]
