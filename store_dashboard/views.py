from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from catalog.models import Product, Category, Brand
from django.contrib import messages
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()

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

@staff_member_required
def dashboard_categories(request):
    if request.method == 'POST':
        name = request.POST.get('category_name')
        if name:
            Category.objects.create(category_name=name)
            messages.success(request, f"Category '{name}' added successfully!")
        return redirect('dashboard_categories')
    categories = Category.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(category_name__icontains=search_query)

    context = {
        'categories': categories,
    }
    return render(request, 'store_dashboard/dashboard_categories.html', context)

@staff_member_required
def edit_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        new_name = request.POST.get('category_name')
        if new_name:
            category.category_name = new_name
            category.save()
            messages.success(request, "Category updated successfully!")
    return redirect('dashboard_categories')

@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    name = category.category_name
    category.delete()
    messages.success(request, f"Category '{name}' was deleted.")
    return redirect('dashboard_categories')

@staff_member_required
def dashboard_brands(request):
    if request.method == 'POST':
        name = request.POST.get('brand_name')
        if name:
            Brand.objects.create(brand_name=name)
            messages.success(request, f"brand '{name}' added successfully!")
        return redirect('dashboard_brands')
    brands = Brand.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        brands = brands.filter(brand_name__icontains=search_query)

    context = {
        'brands': brands,
    }
    return render(request, 'store_dashboard/dashboard_brands.html', context)

@staff_member_required
def edit_brand(request, brand_id):
    if request.method == 'POST':
        brand = get_object_or_404(Brand, id=brand_id)
        new_name = request.POST.get('brand_name')
        if new_name:
            brand.brand_name = new_name
            brand.save()
            messages.success(request, "brand updated successfully!")
    return redirect('dashboard_brands')

@staff_member_required
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    name = brand.brand_name
    brand.delete()
    messages.success(request, f"brand '{name}' was deleted.")
    return redirect('dashboard_brands')

@staff_member_required
def dashboard_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    status_counts = {
        'all': Order.objects.count(),
        'pending': Order.objects.filter(status='Pending').count(),
        'processing': Order.objects.filter(status='Processing').count(),
        'ready': Order.objects.filter(status='Ready').count(),
        'completed': Order.objects.filter(status='Completed').count(),
        'cancelled': Order.objects.filter(status='Cancelled').count(),
    }

    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    sort_by = request.GET.get('sort', 'date_desc')
    if sort_by == 'date_asc':
        orders = orders.order_by('created_at')
    elif sort_by == 'date_desc':
        orders = orders.order_by('-created_at')
    elif sort_by == 'amount_asc':
        orders = orders.order_by('total_price')
    elif sort_by == 'amount_desc':
        orders = orders.order_by('-total_price')

    context = {
        'orders': orders,
        'current_status': status_filter,
        'status_counts': status_counts,
        'search': search_query,
        'sort_by': sort_by, 
    }
    return render(request, 'store_dashboard/dashboard_orders.html', context)

@staff_member_required
def dashboard_order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        if 'update_status' in request.POST:
            # Grab both values from the dropdowns
            order.status = request.POST.get('order_status')
            order.payment_status = request.POST.get('payment_status')
            order.save()
            
            messages.success(request, f"Order #{order.id} has been updated!")
            return redirect('dashboard_order_summary', order_id=order.id)

    context = {
        'order': order,
        'order_items': order.items.all()
    }
    return render(request, 'store_dashboard/dashboard_order_summary.html', context)

@staff_member_required
def dashboard_payments(request):
    payments = Order.objects.all()

    # 1. Handle Search Filter
    search_query = request.GET.get('search', '')
    if search_query:
        payments = payments.filter(
            Q(payment_reference__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(payment_method__icontains=search_query) |
            Q(payment_status__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    # 2. Handle Sort Dropdown
    sort_by = request.GET.get('sort', 'id_asc') # Default sort is id_asc
    if sort_by == 'id_asc':
        payments = payments.order_by('id')
    elif sort_by == 'id_desc':
        payments = payments.order_by('-id')
    elif sort_by == 'date_asc':
        payments = payments.order_by('created_at')
    elif sort_by == 'date_desc':
        payments = payments.order_by('-created_at')
    elif sort_by == 'amount_asc':
        payments = payments.order_by('total_price')
    elif sort_by == 'amount_desc':
        payments = payments.order_by('-total_price')
    elif sort_by == 'status_asc':
        payments = payments.order_by('payment_status')
    elif sort_by == 'status_desc':
        payments = payments.order_by('-payment_status')

    context = {
        'payments': payments,
        'search': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'store_dashboard/dashboard_payments.html', context)

@staff_member_required
def dashboard_home(request):
    orders_summary = Order.objects.aggregate(
        total_orders=Count('id'),
        pending_orders=Count('id', filter=Q(status='Pending')),
        confirmed_orders=Count('id', filter=Q(status='Processing')),
        ready_orders=Count('id', filter=Q(status='Ready')),
        completed_orders=Count('id', filter=Q(status='Completed')),
        cancelled_orders=Count('id', filter=Q(status='Cancelled')),
    )

    total_revenue = Order.objects.filter(status='Completed', payment_status='Paid').aggregate(
        total_sales=Sum('total_price')
    )['total_sales'] or 0

    inventory_summary = Product.objects.aggregate(
        total_products=Count('id'),
        total_stock=Sum('quantity')
    )

    total_users = User.objects.filter(is_staff=False).count()

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(quantity__lt=10).order_by('quantity')[:5]

    context = {
        'orders': orders_summary,
        'total_revenue': total_revenue,
        'total_products': inventory_summary['total_products'] or 0,
        'total_stock': inventory_summary['total_stock'] or 0,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'store_dashboard/dashboard_home.html', context)

@staff_member_required
def dashboard_users(request):
    # --- 1. HANDLE FORM SUBMISSION (ADD / EDIT) ---
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if user_id:
            # EDIT MODE: The hidden user_id field had a value
            target_user = get_object_or_404(User, id=user_id)
            target_user.first_name = first_name
            target_user.last_name = last_name
            target_user.username = username
            target_user.email = email
            target_user.contact_number = contact_number
            target_user.address = address
            
            # If the admin typed a new password, hash it and save it. 
            # If they left it blank, it skips this and keeps the old one!
            if password:
                target_user.set_password(password)
                
            target_user.save()
            messages.success(request, f"User @{target_user.username} has been successfully updated!")
            
        else:
            # ADD MODE: The hidden user_id field was empty
            try:
                new_user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    contact_number=contact_number,
                    address=address
                )
                # Hashes the password securely
                new_user.set_password(password)
                new_user.save()
                messages.success(request, f"New user @{new_user.username} created successfully!")
            except Exception as e:
                # Catches errors like duplicate usernames
                messages.error(request, f"Error creating user: A user with that username or email might already exist.")
        
        return redirect('dashboard_users')

    # --- 2. HANDLE DISPLAY & SEARCH ---
    # Get all users (excluding superusers if you want, but this gets everyone)
    users = User.objects.all().order_by('-date_joined')
    
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'users': users,
    }
    return render(request, 'store_dashboard/dashboard_users.html', context)


@staff_member_required
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    # Safety Check: Prevent the logged-in admin from accidentally deleting themselves!
    if target_user == request.user:
        messages.error(request, "Safety alert: You cannot delete your own admin account.")
    else:
        username = target_user.username
        target_user.delete()
        messages.success(request, f"User @{username} has been permanently deleted.")
        
    return redirect('dashboard_users')