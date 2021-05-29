from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(PotsCategory)
admin.site.register(Pot)
admin.site.register(Review)
admin.site.register(Likes)
admin.site.register(Dislike)
admin.site.register(Order_Pot)
admin.site.register(Potorder)