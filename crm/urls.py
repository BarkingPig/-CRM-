
from crm import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index),  # 首页
    url(r'^salesman/$', views.salesman_index, name = 'salesman_index'),
    url(r'^customer/$', views.customer_index, name = 'customer_index'),
    url(r'^student/$', views.student_index, name = 'student_index'),
]
