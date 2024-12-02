from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BuildYourPizzaForm
from .models import Pizza
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import CartItem


# Create your views here. 

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

            return redirect('cart')  # Redirect to the cart page
    else:
        form = BuildYourPizzaForm()

    return render(request, 'products/build_pizza.html', {'form': form})

#cart view
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == "POST":
        # Remove item from cart
        item_id = request.POST.get("item_id")
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.delete()

    return render(request, 'products/cart.html', {'cart_items': cart_items})
