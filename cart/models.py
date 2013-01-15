from django.db import models

from pizza.models import Pizza
#from cart.views import get_session_cart

# Create your models here.
class Cart(models.Model):
    created_date = models.DateTimeField('date created',auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(*args, **kwargs)
        #items = []

    def add_cart_item(self,product,qty):
        self.save()
        found_item = CartItem.objects.filter(cart = self, product = product)
        if found_item:
            item = found_item[0] 
            item.quantity += int(qty)
        else:
            item = CartItem()
            item.product = product
            item.quantity = qty
            self.items.add(item)
        item.save()
        return item

    def clear(self):
        self.items.all().delete()
        self.delete()

    @property
    def total(self):
        totalCost = 0
        for item in self.items.all():
            totalCost += (item.product.price * item.quantity) 
        return "%.2f" % float(totalCost)

    @property
    def count(self):
        totalCount = 0
        for item in self.items.all():
            totalCount += item.quantity
        return totalCount

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    product = models.ForeignKey(Pizza)
    name = models.CharField(max_length = 60)
    quantity = models.IntegerField(default = 1)

    def __unicode__(self):
        return self.product.name

