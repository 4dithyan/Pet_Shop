from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/', views.create_product_review, name='create_product_review'),
    path('pet/<int:pet_id>/', views.create_pet_review, name='create_pet_review'),
]
