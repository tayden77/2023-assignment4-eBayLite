from django import forms
from django.shortcuts import get_object_or_404
from .models import Listing, Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your bid'}),
        }

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
