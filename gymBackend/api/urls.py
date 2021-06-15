from django.urls import path

from . import views

urlpatterns = [
    path('total_login',views.total_login),
    path('register',views.register),
    path('manager_login',views.Manager_login),
    path('create_class',views.create_class),
    path('get_all_coach', views.get_all_coach),
    path('buy_vipcard', views.buy_vipcard),
    path('buy_class', views.buy_class),
    path('show_all_class', views.show_all_class),
    path('technician_login', views.technician_login),
    path('create_equipment',views.create_Equipment),
    path('create_maintaince', views.create_maintaince),
    path('delete_equipment', views.delete_equipment),
    path('delete_student', views.delete_student),
    path('delete_class', views.delete_class),
    path('customer_class', views.customer_class),
    path('student_get_class',views.student_get_class),

]