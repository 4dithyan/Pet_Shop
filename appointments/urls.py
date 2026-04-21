from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('book-visit/<int:pet_id>/', views.book_visit, name='book_visit'),
    path('book-adoption/<int:pet_id>/', views.book_adoption, name='book_adoption'),
    path('', views.appointment_list, name='appointment_list'),
    path('<int:pk>/approve/', views.approve_appointment, name='approve_appointment'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
