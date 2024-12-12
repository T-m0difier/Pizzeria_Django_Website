from django.shortcuts import render, redirect
from .forms import NewUserForm, UserProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)  # Debug: Output the created user object
            messages.success(request, f"User Created.")
            login(request, user)
            return redirect("/products")

        else:
            print("Form errors:", form.errors)  # Debug form validation issues
    else:
        form = NewUserForm()
    return render(request, "register/register.html", {"register_form": form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_request (request):
    if request.user.is_authenticated:
        return redirect("/products")

    if request.method == "POST":
        form = AuthenticationForm (request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get ('username')
            password = form.cleaned_data.get ('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/products")
            else: 
                messages.error(request, "Invalid username or password.")
    else: 
        form = AuthenticationForm()
    return render(request, "register/login.html", {"login_form": form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_request (request):
    logout(request)
    request.session.flush()  # Clears all session data
    messages.success(request, "You have successfully logged out.")
    return redirect("/login")

# View to display user profile
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def profile(request):
    return render(request, 'register/profile.html', {'user': request.user})

# View to update user credentials (username, email, password)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Handle password update only if the field is not empty
            new_password = form.cleaned_data.get('password')
            if new_password:  # Only update the password if it's provided
                user.set_password(new_password)

            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'register/update_profile.html', {'form': form})