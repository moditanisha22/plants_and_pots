from django.shortcuts import render
from django.views.generic import  CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User 
from .forms import RegisterForm
# Create your views here.
class Registerview(CreateView):
    form_class=RegisterForm
    
    template_name='Account/register.html'
    success_url=reverse_lazy('Account:login')