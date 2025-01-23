from django.db import models

# Create your models here.

class Customer(models.Model):
    fullname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fullname} {self.email} {self.password} {self.phone} {self.address}"

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=20)
    restaurant_cuisines = models.CharField(max_length=20)
    restaurant_address = models.CharField(max_length=20)
    restaurant_rating = models.CharField(max_length=20)
    restaurant_photo = models.URLField(max_length=2000, default="https://cwdaust.com.au/wpress/wp-content/uploads/2015/04/placeholder-restaurant.png")

    def __str__(self):
        return f"{self.restaurant_name} {self.restaurant_cuisines} {self.restaurant_address} {self.restaurant_rating} {self.restaurant_photo}"


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.URLField(max_length=2000, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjjGS5iBKRcrJwPyPm1aXY4uy7KOHZwCj2hA&s")
    is_veg = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.name} {self.description} {self.price} {self.photo}"


class CartList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="cart")
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.menu_item.price

    def __str__(self):
        return f"{self.customer.fullname} - {self.menu_item.name} ({self.quantity})"