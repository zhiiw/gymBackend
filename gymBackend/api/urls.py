from django.urls import path

from . import views

urlpatterns = [
    path('login',views.login),
    path('register',views.register),
    path('manager_login',views.Manager_login),
    path('create_class',views.create_class),
    path('get_all_coach', views.get_all_coach),
    path('buy_vipcard', views.buy_vipcard),
    path('show_all_class', views.show_all_class),
    path('technician_login', views.technician_login),

]