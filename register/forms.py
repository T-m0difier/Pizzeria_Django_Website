from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class NewUserForm(UserCreationForm):  
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileUpdateForm(UserChangeForm):
    # Fields for updating the password
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        required=False,
        label="New password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        required=False,
        label="Confirm new password",
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']  # Exclude 'password' since it is a custom field

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        # Validate that passwords match if provided
        if password or password2:  # Only validate if at least one password field is filled
            if password != password2:
                raise ValidationError("The passwords do not match.")
            
            # Validate password strength using Django's validators
            if password:
                validate_password(password, self.instance)

        return cleaned_data