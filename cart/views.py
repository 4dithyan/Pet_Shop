from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .cart import Cart

def cart_detail(request):
    """
    Display cart contents
    """
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    """
    Add product to cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, override_quantity=False)
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """
    Remove product from cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'{product.name} removed from cart.')
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    """
    Update product quantity in cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, override_quantity=True)
    messages.success(request, 'Cart updated!')
    return redirect('cart:cart_detail')
