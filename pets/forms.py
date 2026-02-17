from django import forms
from .models import Pet, Category

class PetForm(forms.ModelForm):
    """
    Form for adding/editing pets
    """
    class Meta:
        model = Pet
        fields = ['name', 'category', 'breed', 'age_months', 'gender', 'price', 
                  'description', 'is_vaccinated', 'is_available', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class PetCategoryForm(forms.ModelForm):
    """
    Form for adding/editing pet categories
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
