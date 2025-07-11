from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Store
from django import forms

class DatasetUploadForm(forms.Form):
    dataset_file = forms.FileField(label="Upload CSV Dataset", help_text="Upload a training dataset (CSV format).")


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'phone', 'address']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class StoreRegistrationForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

# ✅ NEW FORM: To add a customer to a store by username
class AddCustomerForm(forms.Form):
    username = forms.CharField(label="Customer Username", max_length=150)



class IssueCouponForm(forms.Form):
    amount = forms.DecimalField(label='Coupon Amount', max_digits=8, decimal_places=2)
