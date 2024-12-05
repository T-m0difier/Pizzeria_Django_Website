from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BuildYourPizzaForm
from .models import Pizza, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here. 

def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, "products/index.html", {
        "pizzas": Pizza.objects.all()
    })

def pizza_detail(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    return render(request, "products/pizza_detail.html", {
        "pizza": pizza
    })

def pizza_list(request):
    # Initialize the query with all pizzas
    pizzas = Pizza.objects.all()

    # Get filter parameters
    size_filter = request.GET.get('size', None)
    search_query = request.GET.get('search', None)

    # Apply size filter if provided
    if size_filter:
        pizzas = pizzas.filter(size__name=size_filter)

    # Apply search filter if provided
    if search_query:
        pizzas = pizzas.filter(name__icontains=search_query)

    # Render the response
    return render(request, 'products/index.html', {'pizzas': pizzas})



@login_required
def build_pizza(request):
    if request.method == 'POST':
        form = BuildYourPizzaForm(request.POST)
        if form.is_valid():
            # Gather pizza details
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            crust = form.cleaned_data['crust_type']
            sauce = form.cleaned_data['sauce']
            toppings = form.cleaned_data['toppings']

            # Calculate pizza price
            base_price = 10  # Default base price
            total_price = base_price
            total_price += crust.extra_price
            total_price += sauce.extra_price
            total_price += sum(topping.extra_price for topping in toppings)
            total_price *= size.multiplier
            total_price = round(total_price, 2)

            # Add the pizza to the user's cart
            cart_item = CartItem.objects.create(
                user=request.user,
                pizza_name=name,
                size=size,
                crust=crust,
                sauce=sauce,
                price=total_price
            )
            cart_item.toppings.set(toppings)
            messages.success(request, "Item added to the cart!")
            return redirect('cart')  # Redirect to the cart page
    else:
        form = BuildYourPizzaForm()

    return render(request, 'products/build_pizza.html', {'form': form})

#cart view
@login_required
def cart(request):
    # Fetch all cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate the total price
    total_price = sum(item.price for item in cart_items)

    if request.method == "POST":
        # Handle item removal from the cart
        item_id = request.POST.get("item_id")
        if item_id:
            item = get_object_or_404(CartItem, id=item_id, user=request.user)
            item.delete()
            messages.warning(request, "Item removed from the cart.")
            # Re-fetch cart items after deletion to update the view
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.price for item in cart_items)

    # Render the updated cart
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, pizza_id):
    if request.method == "POST":
        # Fetch the pizza instance
        pizza = get_object_or_404(Pizza, id=pizza_id)

        # Calculate the pizza price dynamically
        pizza_price = pizza.price

        # Create a new CartItem for the logged-in user
        cart_item = CartItem.objects.create(
            user=request.user,
            pizza_name=pizza.name,
            size=pizza.size,
            crust=pizza.crust_type,
            sauce=pizza.sauce,
            price=pizza_price
        )
        cart_item.toppings.set(pizza.toppings.all())

        # Save the cart item
        cart_item.save()

        # Display a success message
        messages.success(request, f"{pizza.name} was added to your cart.")

        # Redirect back to the index page
        return redirect('index')

    return HttpResponse("Invalid request method", status=405)

@login_required
def checkout(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == "POST":
        # Process payment logic or confirmation here
        # For now, we'll just clear the cart
        cart_items.delete()
        messages.success(request, "Thank you for your purchase! Your order is confirmed.")
        return redirect('index')  # Redirect to the homepage after checkout

    # Calculate total price
    total_price = sum(item.price for item in cart_items)
    return render(request, 'products/checkout.html', {'cart_items': cart_items, 'total_price': total_price})