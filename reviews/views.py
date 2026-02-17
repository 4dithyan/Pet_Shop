from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from products.models import Product
from pets.models import Pet

@login_required
def create_product_review(request, product_id):
    """
    Create review for a product
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    if existing_review:
        messages.warning(request, 'You have already reviewed this product.')
        return redirect('products:product_detail', pk=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('products:product_detail', pk=product_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'item': product,
        'item_type': 'product',
    }
    return render(request, 'reviews/create_review.html', context)


@login_required
def create_pet_review(request, pet_id):
    """
    Create review for a pet
    """
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Check if user already reviewed this pet
    existing_review = Review.objects.filter(user=request.user, pet=pet).first()
    if existing_review:
        messages.warning(request, 'You have already reviewed this pet.')
        return redirect('pets:pet_detail', pk=pet_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.pet = pet
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('pets:pet_detail', pk=pet_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'item': pet,
        'item_type': 'pet',
    }
    return render(request, 'reviews/create_review.html', context)
