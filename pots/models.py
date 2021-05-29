from os import replace
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.utils.text import slugify
# Create your models here.

class PotsCategory(models.Model):
    category_name=models.CharField(max_length=40)

    def __str__(self):
        return self.category_name

class Pot(models.Model):
    category=models.ForeignKey(PotsCategory,on_delete=models.CASCADE,related_name='pots')
    pot_name=models.CharField(max_length=40)
    pot_slug=models.SlugField(unique=True)
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
            self.pot_slug=slugify(self.pot_name)
            super().save(*args,**kwargs)

    class Meta:
        ordering=['pot_name']
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
    order_date=models.DateTimeField(default=datetime.now())
    pot=models.ManyToManyField(Pot,related_name='orders',through='Potorder')

    def __str__(self):
            return self.user.username
    
    class Meta:
        ordering=['order_date']

class Potorder(models.Model):
        order=models.ForeignKey(Order_Pot,on_delete=models.CASCADE)
        pot=models.ForeignKey(Pot,on_delete=models.CASCADE)


        def __str__(self):
            return str(self.order.user.username)