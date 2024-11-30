from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Function to generate unique IDs
def generate_unique_id(prefix, model, field_name):
    counter = 1
    unique_id = f"{prefix}{counter}"

    while model.objects.filter(**{field_name: unique_id}).exists():
        counter += 1
        unique_id = f"{prefix}{counter}"

    return unique_id


class Topping(models.Model):
    name = models.CharField(max_length=50)
    vegetarian = models.BooleanField(default=False)
    extra_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    topping_id = models.CharField(max_length=10, unique=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.topping_id}) ({self.extra_price})"


class Sauce(models.Model):
    name = models.CharField(max_length=50)
    extra_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sauce_id = models.CharField(max_length=10, unique=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.sauce_id}) ({self.extra_price})"


class Crust(models.Model):
    type = models.CharField(max_length=50)
    crust_id = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    extra_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.type} ({self.crust_id}) ({self.extra_price})"


class Size(models.Model):
    name = models.CharField(max_length=20)
    multiplier = models.DecimalField(max_digits=4, decimal_places=2)  # Price multiplier based on size
    size_id = models.CharField(max_length=10, unique=True, blank=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.size_id}) ({self.multiplier})"


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    crust_type = models.ForeignKey('Crust', on_delete=models.CASCADE)
    sauce = models.ForeignKey('Sauce', on_delete=models.CASCADE)
    toppings = models.ManyToManyField('Topping', related_name='pizzas')

    # Dynamic Price property
    @property
    def price(self):
        base_price = 10  # Default base price of a pizza
        total_price = base_price

        # Add prices from crust, sauce, and toppings
        total_price += self.crust_type.extra_price
        total_price += self.sauce.extra_price
        total_price += sum(topping.extra_price for topping in self.toppings.all())

        # Apply size multiplier
        total_price *= self.size.multiplier

        return round(total_price, 2)

    def __str__(self):
        return f"{self.name} ({self.size.name}) ({self.id})"


# Signals to automatically generate IDs when each part is saved
@receiver(pre_save, sender=Topping)
def set_topping_id(sender, instance, **kwargs):
    if not instance.topping_id:
        instance.topping_id = generate_unique_id("T", Topping, "topping_id")


@receiver(pre_save, sender=Sauce)
def set_sauce_id(sender, instance, **kwargs):
    if not instance.sauce_id:
        instance.sauce_id = generate_unique_id("Sc", Sauce, "sauce_id")


@receiver(pre_save, sender=Size)
def set_size_id(sender, instance, **kwargs):
    if not instance.size_id:
        instance.size_id = generate_unique_id("Sz", Size, "size_id")


@receiver(pre_save, sender=Crust)
def set_crust_id(sender, instance, **kwargs):
    if not instance.crust_id:
        instance.crust_id = generate_unique_id("C", Crust, "crust_id")
