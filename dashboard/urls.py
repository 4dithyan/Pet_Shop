from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.product_list_admin, name='product_list'),
    path('pets/', views.pet_list_admin, name='pet_list'),
    path('orders/', views.order_list_admin, name='order_list'),
    path('appointments/', views.appointment_list_admin, name='appointment_list'),
]
