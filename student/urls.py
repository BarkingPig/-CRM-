
from student import views
from django.urls import path

urlpatterns = [

    path('$', views.student_index, name='student_index'),  # 别名传前端

]
