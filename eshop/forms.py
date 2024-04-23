from django import forms
from django.contrib.auth.models import User
from  . import models

class UserEshopPC(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","password"]
        widget={
        "first_name":forms.TextInput(attrs={'class':'form-control'}),
        "last_name":forms.TextInput(attrs={'class':'form-control'}),
        "username":forms.TextInput(attrs={'class':'form-control'}),
        "password":forms.PasswordInput(attrs={'class':'form-control'})
        }


class CustomerEshopPC(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=["address","mobile_no","profile_pic"]


class AddressForm(forms.Form):
    Email=forms.EmailField()
    Mobile=forms.IntegerField()
    Address=forms.CharField(max_length=500)


class FeedBackForm(forms.ModelForm):
    class Meta:
        model=models.FeedBack
        fields=['name','email','feedback']
