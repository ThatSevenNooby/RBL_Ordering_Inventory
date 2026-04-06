from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .models import Cart, CartItem, Order, OrderItem

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        messages.success(request, f"Added {quantity}x {product.product_name} to your cart!")
        
        return redirect('product', product_id=product.id)
        
    return redirect('catalog')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    total = sum(item.subtotal for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'customer_cart.html', context)

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')
        
        if action == 'increment':
            if cart_item.quantity < cart_item.product.quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.error(request, f"Sorry, only {cart_item.product.quantity} left in stock.")
                
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete() 
                
        elif action == 'remove':
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.product_name} from your cart.")
            
    return redirect('cart')

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty! Add some items before checking out.")
        return redirect('catalog')

    total = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        reference_number = request.POST.get('reference_number', '')
        proof_image = request.FILES.get('proof_image')

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            payment_method=payment_method,
            payment_reference=reference_number,
            payment_proof=proof_image
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.quantity -= item.quantity
            item.product.save()

        cart.items.all().delete()

        messages.success(request, f"Order #{order.id} has been placed successfully!")
        
        return redirect('order_receipt', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total': total,
        'user': request.user, # Pass the user object so we can show their contact info
    }
    
    return render(request, 'customer_checkout.html', context)

@login_required
def order_receipt(request, order_id):
    # get_object_or_404 ensures the logged-in user actually owns this order!
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'customer_receipt.html', context)