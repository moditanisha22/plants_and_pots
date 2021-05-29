from django.views.generic import *
from pots.models import *

class index(ListView):
    model=Pot
    context_object_name='pot_list'
    template_name='plants_and_pots/base.html'