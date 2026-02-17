from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Product, ProductCategory
from .forms import ProductForm, ProductCategoryForm


def product_list(request):
    """List all products with search and filtering"""
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    # Filter by category
    category_id = request.GET.get('category', '')
    selected_category = None
    if category_id:
        try:
            selected_category = int(category_id)
            products = products.filter(category_id=category_id)
        except ValueError:
            pass
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category
    }
    return render(request, 'shop/items.html', context)


def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/product_detail.html', context)


@staff_member_required
def product_create(request):
    """Create new product (staff only)"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Add Product'})


@staff_member_required
def product_update(request, pk):
    """Update product (staff only)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Edit Product'})


@staff_member_required
def product_delete(request, pk):
    """Delete product (staff only)"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


@staff_member_required
def category_list(request):
    """List all product categories"""
    categories = ProductCategory.objects.all().order_by('name')
    return render(request, 'shop/category_list.html', {'categories': categories})


@staff_member_required
def category_create(request):
    """Create new product category"""
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:category_list')
    else:
        form = ProductCategoryForm()
    
    return render(request, 'shop/category_form.html', {'form': form, 'title': 'Add Category'})


@staff_member_required
def category_update(request, pk):
    """Update product category"""
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('products:category_list')
    else:
        form = ProductCategoryForm(instance=category)
    
    return render(request, 'shop/category_form.html', {'form': form, 'title': 'Edit Category'})


@staff_member_required
def category_delete(request, pk):
    """Delete product category"""
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        return redirect('products:category_list')
    
    return render(request, 'shop/category_confirm_delete.html', {'category': category})
