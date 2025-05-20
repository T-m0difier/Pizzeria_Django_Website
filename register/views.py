from django.shortcuts import render, redirect
from .forms import NewUserForm, UserProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

#register
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User Created.")
            login(request, user)
            return redirect("/products")
        else:
            return render(request, "products/index.html", {
                "register_form": form,
                "register_error": True 
            })

    form = NewUserForm()
    return render(request, "layout.html", {"register_form": form})


#login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_request(request):
    if request.user.is_authenticated:
        return redirect("/products")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("/products")
        return render(request, "products/index.html", {
            "login_form": form,
            "login_error": True
        })

    form = AuthenticationForm()
    return render(request, "layout.html", {"login_form": form})




#logout request view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_request (request):
    logout(request)
    request.session.flush()  # Clears all session data
    messages.success(request, "You have successfully logged out.")
    return redirect("/products")

# View to display user profile
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def profile(request):
    return render(request, 'register/profile.html', {'user': request.user})

# View to update user credentials (username, email, password)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('password')

            # Update password if provided
            if new_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            else:
                user.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("/products")
        else:
            return render(request, "products/index.html", {
                "used_form": form,
                "update_error": True,
                "open_modal" : "updateProfileModal"
            })

    form = UserProfileUpdateForm(instance=request.user)
    return render(request, "register/update_profile.html", {"form": form})