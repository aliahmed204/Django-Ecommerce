from django.db import models
from django.contrib.auth.admin import User 
from datetime import datetime
from decimal import Decimal

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(datetime.now(), default=datetime.now())
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_length=12, max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='images/%y/%m/%d', blank= True)
    is_digital = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(datetime.now())

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''    
        return url

    def __str__(self):
        return self.name
    
class Order(models.Model):

    order_stutes = (
        (1, "pending for payment"),
        (2, "ordered"),
        (3, "shipped"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    total    = models.DecimalField(max_length=12, max_digits=12 , decimal_places=2, default=0.00)
    complete = models.BooleanField(default=False)
    status = models.IntegerField(choices=order_stutes, default=1) 
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def should_shipping(self): # if in order one product not digital would should be shipping
        shipping =False
        for item in self.orderitem_set.all():
            if item.product.is_digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total_price(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total

    @property
    def get_cart_total_qty(self):
        orderItems = self.orderitem_set.all()
        total = sum(item.qty for item in orderItems)   
        return total        
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)    
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        return self.product.price * Decimal(self.qty)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order   = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city    = models.CharField(max_length=200, null=False)
    state   = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
