from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand

def catalog_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    brand_id = request.GET.get('brand')
    if brand_id:
        products = products.filter(brand_id=brand_id)

    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'newest':
        products = products.order_by('-id')
    elif sort_by == 'oldest':
        products = products.order_by('id')
    elif sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('product_name')
    elif sort_by == 'name_desc':
        products = products.order_by('-product_name')
    elif sort_by == 'stock_high':
        products = products.order_by('-quantity')

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_sort': sort_by,
        'product_count': products.count()
    }
    return render(request, 'customer_catalog.html', context)

def product_view(request, product_id):
    single_product = get_object_or_404(Product, id=product_id)

    context = {
        'product': single_product,
    }

    return render(request, 'customer_productpage.html', context)