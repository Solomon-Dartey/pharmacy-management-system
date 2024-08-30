from django import forms
from .models import Drug

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Drug

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from crispy_forms.bootstrap import Field

from .models import Drug

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = [
            'name', 'description', 'quantity', 'unit_price',
            'manufacturing_date', 'expiry_date', 'supplier',
            'generic_name', 'brand_name', 'batch', 'category',
            'packaging_type', 'strength'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
            # Adjust the 'rows' and 'cols' attributes as needed
        }
   
    
# forms.py

from django import forms
from .models import Supplier, Category, PackagingType

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info', 'email']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class PackagingTypeForm(forms.ModelForm):
    class Meta:
        model = PackagingType
        fields = ['type']



# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    phone_number = forms.CharField(max_length=15, required=True)
    # staff_id = forms.CharField(max_length=20, required=True)
    # role = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'phone_number', 'email', 'role', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

