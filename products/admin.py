from django.contrib import admin
from .models import Pizza, Topping, Sauce, Crust, Size

# Register your models here.

admin.site.register(Pizza) 
admin.site.register(Topping)
admin.site.register(Sauce)
admin.site.register(Crust)
admin.site.register(Size)