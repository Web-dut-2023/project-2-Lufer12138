from django.forms import ModelForm
from django import forms
from .models import *

#creating form for user input
class CreateListingForm(ModelForm):
    class Meta:
        model = CreateListing
        #adding felid variables from models
        fields = ['category','title','overview','image','price']
