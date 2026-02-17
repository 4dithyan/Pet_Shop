from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from products.models import Product, InventoryLog

@login_required
def checkout(request):
    """
    Checkout page and order creation
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items and reduce stock
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )
                # Reduce stock
                product.reduce_stock(item['quantity'])
                
                # Log inventory change
                InventoryLog.objects.create(
                    product=product,
                    change_type='REDUCTION',
                    quantity_change=-item['quantity'],
                    previous_quantity=product.stock_quantity + item['quantity'],
                    new_quantity=product.stock_quantity,
                    reason=f'Order {order.order_number}',
                    created_by=request.user
                )
            
            # Clear cart
            cart.clear()
            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        # Pre-fill form with user data
        initial_data = {
            'email': request.user.email,
            'phone': request.user.phone,
        }
        if hasattr(request.user, 'profile'):
            initial_data['shipping_address'] = request.user.profile.address
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    """
    List all orders for current user
    """
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, pk):
    """
    Order detail view
    """
    order = get_object_or_404(Order, pk=pk)
    
    # Check permission
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('orders:order_list')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@staff_member_required
def update_order_status(request, pk):
    """
    Update order status (staff only)
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f'Order status updated to {status}!')
    return redirect('orders:order_detail', pk=pk)
