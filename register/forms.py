from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser  # New user model


#Registration Form
class NewUserForm(UserCreationForm):  
    
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "right",
            "title": "Enter a valid email address.",
        })
    )
    address = forms.CharField(max_length=255, required=True,  widget=forms.TextInput(attrs={
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "right",
            "title": "Provide your full address including street, city, and postal code.",
        })
    )
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "right",
            "title": "Enter a valid phone number (digits only, no spaces).",
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "right",
            "title": "Your password must be at least 8 characters long and should not be too common.",
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "right",
            "title": "Enter the same password again for verification.",
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "data-bs-toggle": "tooltip",
            "data-bs-placement": "right",
            "title": "Usernames must be unique and contain only letters, digits, and @/./+/-/_ characters.",
        })
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone_number']

#Profile update form
class UserProfileUpdateForm(UserChangeForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        required=False,
        label="New Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        required=False,
        label="Confirm New Password"
    )
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}),
        required=True,
        label="Current Password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'phone_number']
        help_texts = {
            'username': '',
            }

        widgets = {
            'username': forms.TextInput(attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "right",
                "title": "Usernames must be unique and contain only letters, digits, and @/./+/-/_ characters.",
            }),
            'email': forms.EmailInput(attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "right",
                "title": "Enter a valid email address.",
            }),
            'address': forms.TextInput(attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "right",
                "title": "Provide your full address.",
            }),
            'phone_number': forms.TextInput(attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "right",
                "title": "Enter a valid phone number (digits only, no spaces).",
            }),
        }


    def clean_address(self):
        address = self.cleaned_data.get("address")
        if not address:
            raise forms.ValidationError("Address cannot be left blank.")
        return address

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('password')
        new_password2 = cleaned_data.get('password2')

        # Always require current password
        if not self.instance.check_password(current_password):
            raise ValidationError("Incorrect current password.")

        # If user started filling in new password, make both required
        if new_password or new_password2:
            if not new_password or not new_password2:
                raise ValidationError("Both new password fields are required.")
            if new_password != new_password2:
                raise ValidationError("The new passwords do not match.")
            validate_password(new_password, self.instance)

        return cleaned_data