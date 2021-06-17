from typing import final
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import *
from .models import *
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from . import Checksum
from django.contrib.auth import get_user_model
import random
user=get_user_model
MERCHANT_KEY="h&CT7oGyf!tTsSg2"
order_value=0

class index(ListView):
    model=Pot
    context_object_name='pot_list'
    template_name='pots/pot_list.html'
    product_list=Pot.objects.all()
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_resin=PotsCategory.objects.filter(category_name__icontains='resin').first()
        category_ceramic=PotsCategory.objects.filter(category_name__icontains='ceramic').first()
        category_metal=PotsCategory.objects.filter(category_name__icontains='metal').first()
        category_hanging=PotsCategory.objects.filter(category_name__icontains='hanging').first()
        print(category_resin.category_name)
        context['resin']=Pot.objects.filter(category=category_resin).order_by('?')[:5]
        context['ceramic']=Pot.objects.filter(category=category_ceramic).order_by('?')[:5]
        context['metal']=Pot.objects.filter(category=category_metal).order_by('?')[:5]
        context['hanging']=Pot.objects.filter(category=category_hanging).order_by('?')[:5]
        context['category_resin']=category_resin.category_name
        context['category_ceramic']=category_ceramic.category_name
        context['category_metal']=category_metal.category_name
        context['category_hanging']=category_metal.category_name
      
        return context
# class Pot_Detail(DetailView):
#     model=Pot 
#     context_object_name='pot_detail'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['query']=Pot.objects.filter(slug__icontains=self.Pot.category.category_name)
#         return context
def Pot_Detail(request,slug,pk):
    pot_detail=Pot.objects.filter(slug=slug).first()
    related_list=Pot.objects.filter(category=PotsCategory.objects.get(pk=pk)).order_by('?')[4:]
    return render(request,'pots/pot_detail.html',{'pot_detail':pot_detail,'related_list':related_list})
@login_required
def AddtoCart(request,slug):
    login='Account:login'
    pot=get_object_or_404(Pot,slug=slug)
    quantity=Quantity_pot.objects.filter(user=request.user,pot=pot)
    try:
       
        cart=AddToCart.objects.filter(user=request.user,pot=pot).first()
        if cart is None :
            AddToCart.objects.create(user=request.user,pot=pot)
             
            
        else:
            print("pass in creating card")
            pass
        quantity=Quantity_pot.objects.filter(user=request.user,pot=pot).first()
        
        print(quantity)
        if quantity is None:
            Quantity_pot.objects.create(user=request.user,pot=pot)
        else:
            obj=get_object_or_404(Quantity_pot,pot=pot,user=request.user)
            if obj.redirect_field==True:
                obj.delete()
                Quantity_pot.objects.create(user=request.user,pot=pot)
            else:
                obj.increase_quantity()

    except:
        pass
    return redirect('pots:cart_list')


# class CartList(ListView):
    
#     template_name='pots/cart_list.html'
#     context_object_name='cart_list'
#     queryset=[]
#     def get_queryset(self):
#         print(self.request.user)
        
#         queryset=AddToCart.objects.order_by('pot').distinct(on_fields='pot')
        
#         return queryset

class CartList(LoginRequiredMixin,ListView):
    login_url='Account:login'
    context_object_name='cart_list'
    template_name='pots/cart_list.html'
    def get_queryset(self):
        final_list=[]
        count=0
        cart= AddToCart.objects.filter(user=self.request.user)
        for i  in range(len(cart)):
            count=0
            for j in range(i+1,len(cart)):
                if(cart[i].pot.slug==cart[j].pot.slug):
                    count+=1
            if count==0:
                final_list.append(cart[i])

            
        return final_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity']=Quantity_pot.objects.filter(user=self.request.user)
        cart= AddToCart.objects.filter(user=self.request.user)
        quantity=Quantity_pot.objects.filter(user=self.request.user)
        sum=0
        price_list=[]
        count=0
        for item in cart:
            sum=0
            for q in quantity:
                if item.pot.slug==q.pot.slug:
                    sum=(item.pot.selling_price)*(q.quantity)
                    price_list.append(sum)
                    

                

            
        for item in price_list:
            count+=item
        context['total_price']=count
        context['price_list']=price_list
        return context
@login_required    
def increse_quantity(request,slug):
    pot=get_object_or_404(Pot,slug=slug)
    quantity=Quantity_pot.objects.filter(user=request.user,pot=pot).first()
    quantity.increase_quantity()
    
    return redirect('pots:cart_list')
@login_required
def decrese_quantity(request,slug):
    pot=get_object_or_404(Pot,slug=slug)
    quantity=Quantity_pot.objects.filter(user=request.user,pot=pot).first()
    quantity.decrease_quantity()
    return redirect('pots:cart_list')

@login_required   
def delete_pot(request,slug):
    pot=get_object_or_404(Pot,slug=slug)

    cart_obj=AddToCart.objects.filter(user=request.user,pot=pot).last()
    quantity=Quantity_pot.objects.get(user=request.user,pot=pot)


    if cart_obj and quantity:
        cart_obj.delete()
        quantity.delete()
        return redirect('pots:cart_list')
    elif(cart_obj is None and quantity):
        quantity.delete()
        return redirect('pots:index')
    else:
        cart_obj.delete()
        quantity.delete()
        return redirect('pots:cart_list')
@login_required
def quick_shop_checkout(request,slug):
    login_url='Account:login'
    pot=get_object_or_404(Pot,slug=slug)

    quantity=Quantity_pot.objects.filter(user=request.user,pot=pot).first()
    if quantity is None:
        pass
        # Quantity_pot.objects.create(user=request.user,pot=pot)
    else:
        quantity.delete()
       
    Quantity_pot.objects.create(user=request.user,pot=pot)
    quantity=Quantity_pot.objects.filter(user=request.user,pot=pot).last()
    quantity.redirect_field=True
    quantity.save()
    print(quantity)
    
    return render(request,'pots/quick_shop_checkout.html',{'pot':pot,'q':quantity})

def quick_increse_quantity(request,slug,pk):
    pot=get_object_or_404(Pot,slug=slug)
    quantity=Quantity_pot.objects.get(pk=pk)
    quantity.increase_quantity()
    
    return render(request,'pots/quick_shop_checkout.html',{'pot':pot,'q':quantity})

def quick_decrese_quantity(request,slug,pk):
    pot=get_object_or_404(Pot,slug=slug)
    quantity=Quantity_pot.objects.get(pk=pk)
    quantity.decrease_quantity()
    return render(request,'pots/quick_shop_checkout.html',{'pot':pot,'q':quantity})


def final_checkout(request):
    cart_list=AddToCart.objects.filter(user=request.user)
    quantity=Quantity_pot.objects.filter(user=request.user)
   
    sum=0
    price_list=[]
    count=0
    for item in cart_list:
        sum=0
        for q in quantity:
            if item.pot.slug==q.pot.slug:
                sum=(item.pot.selling_price)*(q.quantity)
                price_list.append(sum)
                    

    for item in price_list:
        count+=item
   
        
    
    return render(request,'pots/checkout.html',{'cart_list':cart_list,'quantity':quantity,'total_price':count})

def quick_checkout(request,pk):
    quantity=Quantity_pot.objects.get(pk=pk)
    cart_list=Pot.objects.filter(slug=quantity.pot.slug).last()
    form=AddressForm()
    return render(request,'pots/quick_checkout.html',{'cart_list':cart_list,'q':quantity,'form':form})

def quick_final_order(request,pk):
    quantity=Quantity_pot.objects.get(pk=pk)
    # order=Order_Pot.objects.create(user=request.user)
    # final_order=Potorder.objects.create(order=order,pot=quantity.pot)
    param_dict={
        
        "MID": "PKpJIN07261968999081",
        "ORDER_ID": str(pk),
        "CUST_ID": "tanisha.modi.23@gmail.com",
        "TXN_AMOUNT":str(quantity.total_price),
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        'CALLBACK_URL':"http://127.0.0.1:8000/final_response/",
        }
        
    param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)

    return render(request,'pots/paytm.html',{'param_dict':param_dict})
@csrf_exempt
def quick_final_response(request):
    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
           
            print("order success full")
            return redirect("pots:create_order")
           

        else:
            print("not successful" + response_dict['RESPMSG'])
            
    return redirect("pots:cart_list")

def final_order(request):

    
    value=random.randint(111,99999)

    order=Address.objects.filter(user=request.user).order_by('?').first()
    cart_list=AddToCart.objects.filter(user=request.user)
    quantity=Quantity_pot.objects.filter(user=request.user)
  
    sum=0
    price_list=[]
    count=0
    quant=0
    for item in cart_list:
        sum=0
        for q in quantity:
            quant=q.pk
            if item.pot.slug==q.pot.slug:
                sum=(item.pot.selling_price)*(q.quantity)
                price_list.append(sum)
                    

    for item in price_list:
        count+=item

    
  
    print(quant)
    param_dict={
        
        "MID": "PKpJIN07261968999081",
        "ORDER_ID": str(value),
        "CUST_ID": "tanisha.modi.23@gmail.com",
        "TXN_AMOUNT":str(count),
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        'CALLBACK_URL':"http://127.0.0.1:8000/quick_final_response/",
        }
        
    param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)

    return render(request,'pots/paytm.html',{'param_dict':param_dict})

def myorder(request):
    quantity=Quantity_pot.objects.filter(user=request.user)
    return render(request,'pots/myorder.html',{'quantity':quantity})

class all_product(ListView):
    model=Pot
    context_object_name='pot_list'
    template_name='pots/all_product.html'
    product_list=Pot.objects.order_by('?')[1:5]

def search_category(request,category):
    if category=='Resin':
        category=PotsCategory.objects.filter(category_name__icontains=category).first()
    elif category=='Ceramic':
        category=PotsCategory.objects.filter(category_name__icontains=category).first()
    elif category=='Metal':
        category=PotsCategory.objects.filter(category_name__icontains=category).first()
    else:
        category=PotsCategory.objects.filter(category_name__icontains=category).first()
    product_list=Pot.objects.filter(category=category)
    return render(request,'pots/search_product.html',{'product_list':product_list})


def add_address(request):
    address=AddressForm()
    if request.method=='POST':
        address=AddressForm(request.POST)
        if address.is_valid():
            new_address=address.save(commit=False)
            new_address.user=request.user
            new_address.save()
            return redirect('pots:checkout')
        else:
            return redirect('pots:add_address')
    else:
        return render(request,'pots/address.html',{'form':address})      
    return render(request,'pots/address.html',{'form':address})      


def delete_address(request,pk):
    address=Address.objects.get(pk=pk)
    if address:
        address.delete()
        return redirect('pots:checkout')
    else:
        pass

def create_order(request):
    cart_list=AddToCart.objects.filter(user=request.user)
    quantity=Quantity_pot.objects.filter(user=request.user)
    order=Order_Pot.objects.create(user=request.user)
    for cart in cart_list:
        Potorder.objects.create(order=order,pot=cart.pot)
    sum=0
    price_list=[]
    count=0
    
    for item in cart_list:
        sum=0
        for q in quantity:
            if item.pot.slug==q.pot.slug:
                sum=(item.pot.selling_price)*(q.quantity)
                price_list.append(sum)
                    

    for item in price_list:
        count+=item
    return redirect('pots:myorder')



def quick_create_order(request,pk):
    quantity=Quantity_pot.objects.get(pk=pk)
    new_order=Order_Pot.objects.create(user=request.user)
    final_order=Potorder.objects.create(order=new_order,pot=quantity.pot)
    return redirect('pots:myorder')
@csrf_exempt
def final_response(request):
    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
            pk=response_dict['ORDERID']

            print(pk)
            print("order success full")
            return redirect('pots:quick_create_order',pk=pk)
           

        else:
            print("not successful" + response_dict['RESPMSG'])
            
    return redirect("pots:cart_list")