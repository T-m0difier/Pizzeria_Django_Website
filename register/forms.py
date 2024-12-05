from django import forms
from django.contrib.auth import login, authenticate  
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):  
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']





class UserProfileUpdateForm(UserChangeForm):
    # Adding fields for updating the password
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="New password")
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label="Confirm new password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    # Validate that the two password fields match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        
        # If both fields are provided, make sure they match
        if password and password2:
            if password != password2:
                raise forms.ValidationError("The passwords do not match.")
        return cleaned_data