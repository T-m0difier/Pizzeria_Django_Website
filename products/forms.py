from django import forms
from .models import Topping, Sauce, Crust, Size, Pizza
from django.forms import ModelForm


#Staff Capabilities Forms
class ToppingForm(ModelForm):
    class Meta:
        model = Topping
        fields = ['name', 'vegetarian', 'extra_price']

class SauceForm(ModelForm):
    class Meta:
        model = Sauce
        fields = ['name', 'extra_price']

class CrustForm(ModelForm):
    class Meta:
        model = Crust
        fields = ['type', 'extra_price']

class SizeForm(ModelForm):
    class Meta:
        model = Size
        fields = ['name', 'multiplier']

class PizzaForm(ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'image', 'size', 'crust_type', 'sauce', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple,
        }





