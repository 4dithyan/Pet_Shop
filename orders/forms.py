from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    """
    Checkout form for order placement
    """
    class Meta:
        model = Order
        fields = ['payment_method', 'shipping_address', 'phone', 'email']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
