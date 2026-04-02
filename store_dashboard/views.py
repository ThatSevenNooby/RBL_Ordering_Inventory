from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from catalog.models import Product, Category, Brand
from django.contrib import messages

# The @staff_member_required decorator ensures ONLY users with is_staff=True can enter.
@staff_member_required
def dashboard_home(request):
    return render(request, 'store_dashboard/dashboard_home.html')

@staff_member_required
def dashboard_products(request):
    if request.method == 'POST':
        name = request.POST.get('product_name')
        cat_id = request.POST.get('category_id')
        brand_id = request.POST.get('brand_id')
        price = request.POST.get('price')
        qty = request.POST.get('quantity')
        desc = request.POST.get('description')
        
        image = request.FILES.get('image')

        if not cat_id or not brand_id:
            messages.error(request, "Error: You must select both a Category and a Brand.")
            return redirect('dashboard_products')

        category = get_object_or_404(Category, id=cat_id)
        brand = get_object_or_404(Brand, id=brand_id)

        Product.objects.create(
            product_name=name,
            category=category,
            brand=brand,
            price=price,
            quantity=qty,
            description=desc,
            image_path=image
        )
        
        messages.success(request, "Product added successfully!")
        return redirect('dashboard_products')

    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    search_query = request.GET.get('search', '') 
    
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query) |
            Q(brand__brand_name__icontains=search_query)
        )

    sort_by = request.GET.get('sort', 'id_asc')
    
    sort_mapping = {
        'id_asc': 'id',
        'id_desc': '-id',
        'name_asc': 'product_name',
        'name_desc': '-product_name',
        'price_asc': 'price',
        'price_desc': '-price',
        'qty_asc': 'quantity',
        'qty_desc': '-quantity',
    }
    
    order_by_column = sort_mapping.get(sort_by, 'id')
    
    products = products.order_by(order_by_column)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }

    return render(request, 'store_dashboard/dashboard_products.html', context)

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_name = product.product_name 
    product.delete()
    
    messages.success(request, f"'{product_name}' was successfully deleted.")
    return redirect('dashboard_products')

@staff_member_required
def edit_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        product.product_name = request.POST.get('product_name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')
        
        cat_id = request.POST.get('category_id')
        brand_id = request.POST.get('brand_id')
        product.category = get_object_or_404(Category, id=cat_id)
        product.brand = get_object_or_404(Brand, id=brand_id)
        
        if request.FILES.get('image'):
            product.image_path = request.FILES.get('image')
            
        product.save()
        
        messages.success(request, f"'{product.product_name}' was updated successfully!")
        
    return redirect('dashboard_products')