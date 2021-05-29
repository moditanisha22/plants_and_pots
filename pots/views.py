from django.shortcuts import render
from django.views.generic import *
from .models import *

class index(ListView):
    model=Pot
    context_object_name='pot_list'
    template_name='plants_and_pots/base.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_resin=PotsCategory.objects.filter(category_name__icontains='resin').first()
        print(category_resin.category_name)
        context['resin']=Pot.objects.filter(category=category_resin)
        return context
class Pot_Detail(DetailView):
    model=Pot 
    context_object_name='pot_detail'
