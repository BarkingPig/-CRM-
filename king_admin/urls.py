
from king_admin import views
from django.conf.urls import url

urlpatterns = [

    url(r'^$', views.king_admin_index, name="king_admin_index"), # 别名传前端
    url(r'^/(\w+)/(\w+)/$', views.table_index, name="table_index"),
    url(r'^/(\w+)/(\w+)/(\d+)/change/$', views.record_change_index, name="record_change_index"),
    url(r'^/(\w+)/(\w+)/(\d+)/change/password/$', views.record_change_password_index, name="record_change_password_index"),
    url(r'^/(\w+)/(\w+)/add/$', views.record_add_index, name="record_add_index"),
    url(r'^/(\w+)/(\w+)/(\d+)/delete/$', views.record_delete_index, name="record_delete_index"),
]
