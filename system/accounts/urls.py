from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name="login"),
    path('addAdmin/',views.create_admin,name='create_admin'),
    path('listAdmin/',views.admin_list,name='admin_list'),
    path('deleteAdmin/<int:pk>/',views.delete_admin,name='delete_admin'),
    path('logout/',views.logout_view, name='logout'),
]