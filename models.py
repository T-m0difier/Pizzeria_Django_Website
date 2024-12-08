# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CartCart(models.Model):
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart_cart'


class CartCartitem(models.Model):
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(CartCart, models.DO_NOTHING)
    pizza = models.ForeignKey('ProductsPizza', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart_cartitem'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ProductsCartitem(models.Model):
    pizza_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    crust = models.ForeignKey('ProductsCrust', models.DO_NOTHING)
    sauce = models.ForeignKey('ProductsSauce', models.DO_NOTHING)
    size = models.ForeignKey('ProductsSize', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_cartitem'


class ProductsCartitemToppings(models.Model):
    cartitem = models.ForeignKey(ProductsCartitem, models.DO_NOTHING)
    topping = models.ForeignKey('ProductsTopping', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_cartitem_toppings'
        unique_together = (('cartitem', 'topping'),)


class ProductsCrust(models.Model):
    type = models.CharField(max_length=50)
    crust_id = models.CharField(unique=True, max_length=10)
    extra_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'products_crust'


class ProductsOrder(models.Model):
    created_at = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    is_completed = models.BooleanField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_order'


class ProductsOrderitem(models.Model):
    pizza_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    crust = models.ForeignKey(ProductsCrust, models.DO_NOTHING)
    order = models.ForeignKey(ProductsOrder, models.DO_NOTHING)
    sauce = models.ForeignKey('ProductsSauce', models.DO_NOTHING)
    size = models.ForeignKey('ProductsSize', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_orderitem'


class ProductsOrderitemToppings(models.Model):
    orderitem = models.ForeignKey(ProductsOrderitem, models.DO_NOTHING)
    topping = models.ForeignKey('ProductsTopping', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_orderitem_toppings'
        unique_together = (('orderitem', 'topping'),)


class ProductsPizza(models.Model):
    name = models.CharField(max_length=100)
    crust_type = models.ForeignKey(ProductsCrust, models.DO_NOTHING)
    sauce = models.ForeignKey('ProductsSauce', models.DO_NOTHING)
    size = models.ForeignKey('ProductsSize', models.DO_NOTHING)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_pizza'


class ProductsPizzaToppings(models.Model):
    pizza = models.ForeignKey(ProductsPizza, models.DO_NOTHING)
    topping = models.ForeignKey('ProductsTopping', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_pizza_toppings'
        unique_together = (('pizza', 'topping'),)


class ProductsSauce(models.Model):
    name = models.CharField(max_length=50)
    extra_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sauce_id = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'products_sauce'


class ProductsSize(models.Model):
    name = models.CharField(max_length=20)
    multiplier = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    size_id = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'products_size'


class ProductsTopping(models.Model):
    name = models.CharField(max_length=50)
    vegetarian = models.BooleanField()
    extra_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    topping_id = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'products_topping'
