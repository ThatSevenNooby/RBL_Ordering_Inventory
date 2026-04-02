from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
]