from .forms import NewUserForm, UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm

def auth_forms(request):
    return {
        'login_form': AuthenticationForm(),
        'register_form': NewUserForm(),
    }

def update_profile_form(request):
    if request.user.is_authenticated:
        return {'update_profile_form': UserProfileUpdateForm(instance=request.user)}
    return {}