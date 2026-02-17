from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Pet, Category
from .forms import PetForm, PetCategoryForm

def pet_list(request):
    """
    Display all available pets with filtering and search
    """
    pets = Pet.objects.filter(is_available=True)
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        pets = pets.filter(category__slug=category_slug)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) | 
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query or '',
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    """
    Display detailed pet information
    """
    pet = get_object_or_404(Pet, pk=pk)
    related_pets = Pet.objects.filter(category=pet.category, is_available=True).exclude(pk=pk)[:4]
    
    context = {
        'pet': pet,
        'related_pets': related_pets,
    }
    return render(request, 'pets/pet_detail.html', context)


@staff_member_required
def pet_create(request):
    """
    Create new pet (staff only)
    """
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet added successfully!')
            return redirect('pets:pet_list')
    else:
        form = PetForm()
    
    return render(request, 'pets/pet_form.html', {'form': form, 'action': 'Add'})


@staff_member_required
def pet_update(request, pk):
    """
    Update pet details (staff only)
    """
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet updated successfully!')
            return redirect('pets:pet_detail', pk=pk)
    else:
        form = PetForm(instance=pet)
    
    return render(request, 'pets/pet_form.html', {'form': form, 'action': 'Update', 'pet': pet})


@staff_member_required
def pet_delete(request, pk):
    """
    Delete pet (staff only)
    """
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet deleted successfully!')
        return redirect('pets:pet_list')
    
    
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})


@staff_member_required
def category_list(request):
    """List all pet categories"""
    categories = Category.objects.all().order_by('name')
    return render(request, 'pets/category_list.html', {'categories': categories})


@staff_member_required
def category_create(request):
    """Create new pet category"""
    if request.method == 'POST':
        form = PetCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('pets:category_list')
    else:
        form = PetCategoryForm()
    
    return render(request, 'pets/category_form.html', {'form': form, 'title': 'Add Pet Category'})


@staff_member_required
def category_update(request, pk):
    """Update pet category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = PetCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('pets:category_list')
    else:
        form = PetCategoryForm(instance=category)
    
    return render(request, 'pets/category_form.html', {'form': form, 'title': 'Edit Pet Category'})


@staff_member_required
def category_delete(request, pk):
    """Delete pet category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('pets:category_list')
    
    return render(request, 'pets/category_confirm_delete.html', {'category': category})
