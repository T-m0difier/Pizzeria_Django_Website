from django import forms
from .models import Topping, Sauce, Crust, Size, Pizza
from django.forms import ModelForm

class BuildYourPizzaForm(forms.Form):
    name = forms.CharField(max_length=100, label="Pizza Name", required=True)
    size = forms.ModelChoiceField(queryset=Size.objects.all(), label="Size", required=True)
    crust_type = forms.ModelChoiceField(queryset=Crust.objects.all(), label="Crust", required=True)
    sauce = forms.ModelChoiceField(queryset=Sauce.objects.all(), label="Sauce", required=True)
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': '5'}),  # size is optional, just changes the number of visible options
        label="Toppings",
        required=False
    )


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
        fields = ['name', 'size', 'crust_type', 'sauce', 'toppings']





