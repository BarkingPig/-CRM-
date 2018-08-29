
from king_admin import views
from django.conf.urls import url

urlpatterns = [

    url(r'^$', views.king_admin_index, name="king_admin_index"), # 别名传前端
    url(r'^/(\w+)/(\w+)/$', views.table_index, name="table_index"),

]
