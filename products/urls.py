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
    

]
