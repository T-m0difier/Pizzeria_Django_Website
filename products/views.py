from django.http import HttpResponse
from django.shortcuts import render
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
