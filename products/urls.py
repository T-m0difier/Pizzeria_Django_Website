from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Products Page
    path("pizza/<int:pizza_id>/", views.pizza_detail, name="pizza_detail"),
    path("pizzas/", views.pizza_list, name="pizza_list"),  # Filtering & Searching Functionality
    path('build/', views.build_pizza, name='build_pizza'), # Pizza Building Functionality
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path("order_history/", views.order_history, name="order_history"),

    # Staff Abilities URLS
    # Toppings
    path('staff/manage_toppings/', views.manage_toppings, name='manage_toppings'),
    path('staff/manage_toppings/edit/<int:topping_id>/', views.edit_topping, name='edit_topping'),

    # Sauces
    path('staff/manage_sauces/', views.manage_sauces, name='manage_sauces'),
    path('staff/manage_sauces/edit/<int:sauce_id>/', views.edit_sauce, name='edit_sauce'),

    # Crusts
    path('staff/manage_crusts/', views.manage_crusts, name='manage_crusts'),
    path('staff/manage_crusts/edit/<int:crust_id>/', views.edit_crust, name='edit_crust'),

    # Sizes
    path('staff/manage_sizes/', views.manage_sizes, name='manage_sizes'),
    path('staff/manage_sizes/edit/<int:size_id>/', views.edit_size, name='edit_size'),

    # Pizzas
    path('staff/manage_pizzas/', views.manage_pizzas, name='manage_pizzas'),
    path('staff/manage_pizzas/edit/<int:pizza_id>/', views.edit_pizza, name='edit_pizza'),
    
    # Portal
    path('staff/portal/', views.staff_portal, name='staff_portal'),
]
