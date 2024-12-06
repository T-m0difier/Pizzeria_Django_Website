from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BuildYourPizzaForm
from .models import Pizza, Size, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control


# Create your views here. 

def home(request):
    return render(request, 'home.html')


def index(request):
    pizzas = Pizza.objects.all()
    available_sizes = Size.objects.all()
    return render(request, 'products/index.html', {
        'pizzas': pizzas,
        'available_sizes': available_sizes,
    })

def pizza_detail(request, pizza_id):
    pizza = Pizza.objects.get(id=pizza_id)
    return render(request, "products/pizza_detail.html", {
        "pizza": pizza
    })

def pizza_list(request):
    # Fetch all pizzas
    pizzas = Pizza.objects.all()

    # Get all available sizes dynamically
    available_sizes = Size.objects.all()

    # Filter parameters
    size_filter = request.GET.get('size', None)
    search_query = request.GET.get('search', None)

    # Apply size filter
    if size_filter:
        pizzas = pizzas.filter(size__name=size_filter)

    # Apply search filter
    if search_query:
        pizzas = pizzas.filter(name__icontains=search_query)

    return render(request, 'products/index.html', {
        'pizzas': pizzas,
        'available_sizes': available_sizes,
    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def checkout(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == "POST":
        # Create a new order
        total_price = sum(item.price for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Create order items
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                pizza_name=item.pizza_name,
                size=item.size,
                crust=item.crust,
                sauce=item.sauce,
                price=item.price,
            )
            order_item.toppings.set(item.toppings.all())

        # Clear the cart
        cart_items.delete()
        messages.success(request, "Thank you for your purchase! Your order is confirmed.")

        # Redirect to the order history page
        return redirect('order_history')  # Create this URL and view later

    # Calculate total price
    total_price = sum(item.price for item in cart_items)
    return render(request, 'products/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def order_history(request):
    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        action = request.POST.get("action")

        if order_id and action:
            order = get_object_or_404(Order, id=order_id, user=request.user)

            if action == "delete":
                order.delete()
                messages.success(request, "Order deleted successfully.")
            elif action == "repeat":
                # Add the order items back to the cart
                for item in order.items.all():
                    cart_item = CartItem.objects.create(
                        user=request.user,
                        pizza_name=item.pizza_name,
                        size=item.size,
                        crust=item.crust,
                        sauce=item.sauce,
                        price=item.price,
                    )
                    cart_item.toppings.set(item.toppings.all())
                messages.success(request, "Order added back to your cart.")
                return redirect('cart')

    return render(request, 'products/order_history.html', {'orders': orders})