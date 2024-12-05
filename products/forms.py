from django import forms
from .models import Topping, Sauce, Crust, Size

class BuildYourPizzaForm(forms.Form):
    name = forms.CharField(max_length=100, label="Pizza Name", required=True)
    size = forms.ModelChoiceField(queryset=Size.objects.all(), label="Size", required=True)
    crust_type = forms.ModelChoiceField(queryset=Crust.objects.all(), label="Crust", required=True)
    sauce = forms.ModelChoiceField(queryset=Sauce.objects.all(), label="Sauce", required=True)
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Toppings",
        required=False
    )