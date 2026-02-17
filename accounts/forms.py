from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import User, Profile

class UserLoginForm(forms.Form):
    """
    Custom login form accepting email or phone
    """
    username = forms.CharField(label="Email or Phone Number", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email or phone'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserRegisterForm(UserCreationForm):
    """
    User registration form with role selection
    """
    full_name = forms.CharField(label="Full Name", max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text
        self.fields['phone'].help_text = None
        if 'password1' in self.fields:
             self.fields['password1'].help_text = None
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('full_name'),
            Field('email'),
            Field('phone'),
            Field('password1'),
            Field('password2'),
            Submit('submit', 'Register', css_class='btn btn-primary w-100')
        )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            # Generate username from email
            username = email.split('@')[0]
            # Ensure uniqueness
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            cleaned_data['username'] = username
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    User update form for profile editing
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']


class ProfileUpdateForm(forms.ModelForm):
    """
    Profile update form for additional information
    """
    class Meta:
        model = Profile
        fields = ['image', 'address', 'city', 'state', 'pincode']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
