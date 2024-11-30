from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)  # Debug: Output the created user object
            login(request, user)
            return redirect("/products")

        else:
            print("Form errors:", form.errors)  # Debug form validation issues
    else:
        form = NewUserForm()
    return render(request, "register/register.html", {"register_form": form})


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

def logout_request (request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/login")