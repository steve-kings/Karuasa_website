from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class MemberRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address'
    }))
    registration_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your registration number'
    }))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., 0712345678'
    }))
    member_type = forms.ChoiceField(choices=Member.MEMBER_TYPES, required=True, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    course = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., BSc Actuarial Science'
    }))
    year_of_study = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g., 2',
        'min': '1',
        'max': '5'
    }))
    
    class Meta:
        model = Member
        fields = ['username', 'email', 'first_name', 'last_name', 'registration_number', 
                 'phone_number', 'member_type', 'course', 'year_of_study', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Create a password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password'
            }),
        }

class MemberUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    course = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    year_of_study = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'min': '1',
        'max': '5'
    }))
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'course', 'year_of_study', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }