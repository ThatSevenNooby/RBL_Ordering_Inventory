from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),

    path('categories/', views.dashboard_categories, name='dashboard_categories'),
    path('categories/add/', views.dashboard_categories, name='add_category'), # Reuses the main view
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    path('brands/', views.dashboard_brands, name='dashboard_brands'),
    path('brands/add/', views.dashboard_brands, name='add_brand'), # Reuses the main view
    path('brands/edit/<int:brand_id>/', views.edit_brand, name='edit_brand'),
    path('brands/delete/<int:brand_id>/', views.delete_brand, name='delete_brand'),

    path('orders/', views.dashboard_orders, name='dashboard_orders'),
    path('orders/<int:order_id>/', views.dashboard_order_summary, name='dashboard_order_summary'),

    path('payments/', views.dashboard_payments, name='dashboard_payments'),
]