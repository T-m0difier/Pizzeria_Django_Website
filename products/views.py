from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ToppingForm, SauceForm, CrustForm, SizeForm, PizzaForm
from .models import Pizza, Size, CartItem, Order, OrderItem, Crust, Sauce, Topping
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.db.models import Count

# Create your views here. 
#Homepage view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html')

#Index/Products page view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    pizzas = Pizza.objects.all()
    available_sizes = Size.objects.all()

    # Include data required for customization modals
    sizes = Size.objects.all()
    crusts = Crust.objects.all()
    sauces = Sauce.objects.all()
    all_toppings = Topping.objects.all()

    return render(request, 'products/index.html', {
        'pizzas': pizzas,
        'available_sizes': available_sizes,
        'sizes': sizes,
        'crusts': crusts,
        'sauces': sauces,
        'all_toppings': all_toppings,
    })

#Filtering + Searching Functionalities View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pizza_list(request):
    pizzas = Pizza.objects.all()
    available_sizes = Size.objects.all()

    # Fetch all data needed for customization modals
    sizes = Size.objects.all()
    crusts = Crust.objects.all()
    sauces = Sauce.objects.all()
    all_toppings = Topping.objects.all()

    # Filter parameters
    size_filter = request.GET.get('size')
    search_query = request.GET.get('search')

    if size_filter:
        pizzas = pizzas.filter(size__name=size_filter)

    if search_query:
        pizzas = pizzas.filter(name__icontains=search_query)

    open_modal = request.session.pop('open_modal', None)

    return render(request, 'products/index.html', {
        'pizzas': pizzas,
        'available_sizes': available_sizes,
        'sizes': sizes,
        'crusts': crusts,
        'sauces': sauces,
        'all_toppings': all_toppings,
        'open_modal': open_modal,
    })

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


#Add to cart view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def add_to_cart(request, pizza_id):
    if request.method == "POST":
        pizza = get_object_or_404(Pizza, id=pizza_id)
        
        # Get customization from POST
        size_id = request.POST.get("size")
        crust_id = request.POST.get("crust")
        sauce_id = request.POST.get("sauce")
        topping_ids = request.POST.getlist("toppings")
        quantity = int(request.POST.get("quantity", 1))

        # Fetch related objects
        size = get_object_or_404(Size, id=size_id) if size_id else pizza.size
        crust = get_object_or_404(Crust, id=crust_id) if crust_id else pizza.crust_type
        sauce = get_object_or_404(Sauce, id=sauce_id) if sauce_id else pizza.sauce
        toppings = Topping.objects.filter(id__in=topping_ids) if topping_ids else pizza.toppings.all()

        possible_items = CartItem.objects.filter(
            user = request.user,
            size = size,
            crust = crust,
            sauce = sauce).annotate(num_toppings = Count('toppings')).filter(num_toppings=toppings.count())

        for item in possible_items:
            if set(item.toppings.all()) == set(toppings):
                item.quantity += quantity
                item.price += (item.price / (item.quantity -quantity)) * quantity
                item.save()
                messages.success(request, f"Updated cart.")
                return redirect('index')

        # Calculate price per pizza
        base_price = 10
        price = base_price + crust.extra_price + sauce.extra_price + sum(t.extra_price for t in toppings)
        price *= size.multiplier
        total_price = round(price * quantity, 2)

        # Create cart item
        cart_item = CartItem.objects.create(
            user=request.user,
            pizza_name=pizza.name,
            size=size,
            crust=crust,
            sauce=sauce,
            price=total_price,
            quantity=quantity
        )
        cart_item.toppings.set(toppings)
        cart_item.save()

        messages.success(request, f"{pizza.name} (x{quantity}) was added to your cart.")
        return redirect("index")

    return HttpResponse("Invalid request method", status=405)


#Checkout view
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
                quantity=item.quantity
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

#Order History view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def order_history(request):
    # Fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        action = request.POST.get("action")

        if order_id and action == "repeat":
            order = get_object_or_404(Order, id=order_id, user=request.user)
            
            
            #Clear the Cart before repeating an order
            CartItem.objects.filter(user=request.user).delete()

            # Add the order items back to the cart
            for item in order.items.all():
                cart_item = CartItem.objects.create(
                    user=request.user,
                    pizza_name=item.pizza_name,
                    size=item.size,
                    crust=item.crust,
                    sauce=item.sauce,
                    price=item.price,
                    quantity=item.quantity
                )
                cart_item.toppings.set(item.toppings.all())
            messages.success(request, "Order added back to your cart.")
            return redirect('cart')

    return render(request, 'products/order_history.html', {'orders': orders})

#From this point on, the views are for the staff capabilities

def staff_required(user):
    return user.is_staff

# Staff Manage Toppings
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def manage_toppings(request):
    if request.method == "POST":
        form = ToppingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Topping saved successfully.")
            return redirect('manage_toppings')
    else:
        form = ToppingForm()

    toppings = Topping.objects.all()
    return render(request, 'staff/manage_toppings.html', {
        'form': form,
        'toppings': toppings,
    })

#Edit toppings
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def edit_topping(request, topping_id):
    topping = get_object_or_404(Topping, id=topping_id)
    if request.method == "POST":
        form = ToppingForm(request.POST, instance=topping)
        if form.is_valid():
            form.save()
            messages.success(request, "Topping updated successfully.")
            return redirect('manage_toppings')
    else:
        form = ToppingForm(instance=topping)

    return render(request, 'staff/edit_topping.html', {
        'form': form,
    })


# Staff Manage Sauces
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def manage_sauces(request):
    if request.method == "POST":
        form = SauceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sauce saved successfully.")
            return redirect('manage_sauces')
    else:
        form = SauceForm()

    sauces = Sauce.objects.all()
    return render(request, 'staff/manage_sauces.html', {
        'form': form,
        'sauces': sauces,
    })

#Edit sauces
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def edit_sauce(request, sauce_id):
    sauce = get_object_or_404(Sauce, id=sauce_id)
    if request.method == "POST":
        form = SauceForm(request.POST, instance=sauce)
        if form.is_valid():
            form.save()
            messages.success(request, "Sauce updated successfully.")
            return redirect('manage_sauces')
    else:
        form = SauceForm(instance=sauce)

    return render(request, 'staff/edit_sauce.html', {
        'form': form,
    })

# Staff Manage Crusts
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def manage_crusts(request):
    if request.method == "POST":
        form = CrustForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Crust saved successfully.")
            return redirect('manage_crusts')
    else:
        form = CrustForm()

    crusts = Crust.objects.all()
    return render(request, 'staff/manage_crusts.html', {
        'form': form,
        'crusts': crusts,
    })

#Edit crusts
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def edit_crust(request, crust_id):
    crust = get_object_or_404(Crust, id=crust_id)
    if request.method == "POST":
        form = CrustForm(request.POST, instance=crust)
        if form.is_valid():
            form.save()
            messages.success(request, "Crust updated successfully.")
            return redirect('manage_crusts')
    else:
        form = CrustForm(instance=crust)

    return render(request, 'staff/edit_crust.html', {
        'form': form,
    })

# Staff Manage Sizes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def manage_sizes(request):
    if request.method == "POST":
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Size saved successfully.")
            return redirect('manage_sizes')
    else:
        form = SizeForm()

    sizes = Size.objects.all()
    return render(request, 'staff/manage_sizes.html', {
        'form': form,
        'sizes': sizes,
    })
#Edit sizes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def edit_size(request, size_id):
    size = get_object_or_404(Size, id=size_id)
    if request.method == "POST":
        form = SizeForm(request.POST, instance=size)
        if form.is_valid():
            form.save()
            messages.success(request, "Size updated successfully.")
            return redirect('manage_sizes')
    else:
        form = SizeForm(instance=size)

    return render(request, 'staff/edit_size.html', {
        'form': form,
    })

# Staff Manage Pizzas
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def manage_pizzas(request):
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pizza saved successfully.")
            return redirect('manage_pizzas')
    else:
        form = PizzaForm()

    pizzas = Pizza.objects.all()
    return render(request, 'staff/manage_pizzas.html', {
        'form': form,
        'pizzas': pizzas,
    })

#Edit pizzas
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def edit_pizza(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
            messages.success(request, "Pizza updated successfully.")
            return redirect('manage_pizzas')
    else:
        form = PizzaForm(instance=pizza)

    return render(request, 'staff/edit_pizza.html', {
        'form': form,
    })

#Staff portal view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(staff_required)
def staff_portal(request):
    return render(request, 'staff/portal.html')