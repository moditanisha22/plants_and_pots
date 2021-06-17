from django import forms 
from .models import Address
class AddressForm(forms.ModelForm):
    

    class Meta():
        model=Address
        fields=('first_name', 'last_name', 'email', 'mobile_no', 'flat_no','Area_Colony','Landmark', 'Town_City', 'State', 'Pincode')
