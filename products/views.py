from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BuildYourPizzaForm
from .models import Pizza


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


def build_pizza(request):
    if request.method == 'POST':
        form = BuildYourPizzaForm(request.POST)
        if form.is_valid():
            # Create a new Pizza object
            size = form.cleaned_data['size']
            crust_type = form.cleaned_data['crust_type']
            sauce = form.cleaned_data['sauce']
            toppings = form.cleaned_data['toppings']
            name = form.cleaned_data['name']

            # Create and save the pizza object
            pizza = Pizza.objects.create(
                name=name,
                size=size,
                crust_type=crust_type,
                sauce=sauce
            )
            pizza.toppings.set(toppings)
            pizza.save()

            # Redirect to the pizza list or confirmation page
            return redirect('index')  # Update to your desired redirect
    else:
        form = BuildYourPizzaForm()

    return render(request, 'products/build_pizza.html', {'form': form})





