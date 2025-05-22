from django.contrib import admin
from .models import Pizza, Topping, Sauce, Crust, Size
from django import forms

class PizzaAdminForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = '__all__'
        widgets ={
            'toppings': forms.CheckboxSelectMultiple
        }

class PizzaAdmin(admin.ModelAdmin):
    form = PizzaAdminForm
    
admin.site.register(Pizza, PizzaAdmin) 
admin.site.register(Topping)
admin.site.register(Sauce)
admin.site.register(Crust)
admin.site.register(Size)




