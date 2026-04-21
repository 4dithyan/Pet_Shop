from django.shortcuts import render
from pets.models import Pet

def home(request):
    """Home page view"""
    # Get 3 available pets to feature on the homepage
    featured_pets = Pet.objects.filter(is_available=True)[:3]
    return render(request, 'home.html', {'featured_pets': featured_pets})

