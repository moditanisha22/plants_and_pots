from os import replace
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.base import Model
from django.db.models.fields.related import RelatedField
from django.shortcuts import get_object_or_404

from django.utils.text import slugify
# Create your models here.

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='address')
    first_name=models.CharField(max_length=40,default=" ")
    last_name=models.CharField(max_length=40,default=" ")
    email=models.EmailField(default=" ")
    mobile_no=models.CharField(max_length=12)
    flat_no=models.CharField(max_length=10,default="1-A")
    Area_Colony=models.CharField(max_length=200)
    Landmark=models.CharField(max_length=100)
    Town_City=models.CharField(max_length=20)
    State=models.CharField(max_length=20)
    Pincode=models.CharField(max_length=6)

    def __str__(self):
        return self.Pincode

    class Meta:
        ordering=['Pincode','user']

class PotsCategory(models.Model):
    category_name=models.CharField(max_length=40)

    def __str__(self):
        return self.category_name

class Pot(models.Model):
    category=models.ForeignKey(PotsCategory,on_delete=models.CASCADE,related_name='pots')
    pot_name=models.CharField(max_length=60)
    slug=models.SlugField()
    marked_price=models.IntegerField()
    pot_description=models.TextField()
    pot_color=models.CharField(max_length=30)
    pot_size=models.CharField(max_length=70)
    selling_price=models.IntegerField(null=True)
    pot_image=models.ImageField(upload_to='images',blank=True, null=True)
    pot_rating=models.SmallIntegerField()
   

    def __str__(self):
        return self.pot_name 
    def save(self,*args,**kwargs):
            self.slug=slugify(self.pot_name)
            super().save(*args,**kwargs)
   


    class Meta:
        ordering=['-pot_name']
class Review(models.Model):
    pot=models.ForeignKey(Pot,on_delete=models.CASCADE,related_name='pots')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    review=models.TextField()
    review_image=models.ImageField(upload_to='pots/images' , blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
    class Meta:
        ordering=['user','pot']
    
class Likes(models.Model):
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='likes')
    user=models.ForeignKey(User,on_delete=models.CASCADE,name='likes')

    class Meta:
        ordering=['review']

class Dislike(models.Model):
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='dislikes')
    user=models.ForeignKey(User,on_delete=models.CASCADE,name='dislikes')

class Order_Pot(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    address=models.ForeignKey(Address,on_delete=models.CASCADE,related_name='order',default=1)
    order_date=models.DateTimeField(default=datetime.now())
    pot=models.ManyToManyField(Pot,related_name='orders',through='Potorder')

    def __str__(self):
            return self.user.username
    
    class Meta:
        ordering=['-order_date']

class Potorder(models.Model):
        order=models.ForeignKey(Order_Pot,on_delete=models.CASCADE)
        pot=models.ForeignKey(Pot,on_delete=models.CASCADE)


        def __str__(self):
            return str(self.order.user.username)

class Property(models.Model):
    category=models.ForeignKey(PotsCategory,related_name='property',on_delete=models.CASCADE)
    prop=models.CharField(max_length=100)

    def __str__(self):
        return self.prop

class AddToCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    pot=models.ForeignKey(Pot,on_delete=models.CASCADE,related_name='cart')

    def __str__(self):
        return self.pot.pot_name

class Quantity_pot(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='quantity')
    pot=models.ForeignKey(Pot,on_delete=models.CASCADE,related_name='pot_quantity')
    quantity=models.SmallIntegerField(default=1)
    total_price=models.SmallIntegerField(default=1)
    redirect_field=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.total_price=(self.quantity)*(self.pot.selling_price)
        super().save(*args, **kwargs) 

    def increase_quantity(self):
        self.quantity=(self.quantity)+1
        self.total_price=(self.quantity)*(self.pot.selling_price)
        self.save()
    def decrease_quantity(self):
        if self.quantity>1:
            self.quantity=(self.quantity)-1
            self.total_price=(self.quantity)*(self.pot.selling_price)
            self.save()
        else:
            cart=AddToCart.objects.filter(user=self.user,pot=self.pot).first()
            cart.delete()
            self.delete()
            
            
    def __str__(self):
        return self.pot.pot_name

