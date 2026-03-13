from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand

# Create your views here.
def catalog_view(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    all_brands = Brand.objects.all()
    context = {
        'products': all_products,
        'categories': all_categories,
        'brands': all_brands,
    }
    return render(request, 'customer_catalog.html', context)

def product_view(request, product_id):
    single_product = get_object_or_404(Product, id=product_id)

    context = {
        'product': single_product,
    }

    return render(request, 'customer_productpage.html', context)
