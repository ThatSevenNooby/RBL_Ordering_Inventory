"""
URL configuration for RBL_Ordering_Inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import login_view, logout_view
from catalog.views import catalog_view, product_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', include('store_dashboard.urls')),

    path('', TemplateView.as_view(template_name='customer_home.html'), name='home'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('register/', TemplateView.as_view(template_name='customer_register.html'), name='register'),
    path('catalog/', catalog_view, name='catalog'),
    path('product/<int:product_id>/', product_view, name='product'),
]
