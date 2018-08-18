
from king_admin import views
from django.urls import path

urlpatterns = [

    path('$/', views.king_admin_index), # 别名传前端
    path('table', views.table_index),

]
