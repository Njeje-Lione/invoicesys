from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='dashboard'),
    path('addClient/',views.add_client,name="add_client"),
    path('list/<str:app_name>/<str:model_name>/', views.list_objects, name='list_objects'),
    path('deleteClient/<int:pk>/',views.delete_client,name='delete_client'),
    path('invoice/',views.create_invoice,name="create_invoice"),
    path('charges/<int:invoice_id>',views.charges,name="charges"),
    path('deleteInvoice/<int:pk>/',views.delete_invoice,name='delete_invoice'),
    path('invoice/<int:invoice_id>/pdf/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
]