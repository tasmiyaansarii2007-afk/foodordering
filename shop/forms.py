from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "phone", "address", "city", "postal_code")
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError("Enter a valid phone number (at least 10 digits).")
        return phone
