from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser
from orders.models import Order

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('dashboard_home')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
        
    return render(request, 'customer_login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        middle_name = request.POST.get('middlename')
        last_name = request.POST.get('lastname')
        birthdate = request.POST.get('birthdate')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone') 
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
            
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken!")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with that email already exists!")
            return redirect('register')

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,    
                contact_number=phone,       
                address=address,            
                birthdate=birthdate         
            )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register')

    return render(request, 'customer_register.html')

def profile_view(request):
    active_tab = request.GET.get('tab', 'account')
    
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'user': request.user,
        'active_tab': active_tab,
        'orders': user_orders,
    }
    
    return render(request, 'customer_profile.html', context)