from django import forms
from django.shortcuts import get_object_or_404
from .models import Listing, Bid


class BidForm(forms.ModelForm):
    listing_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Bid
        fields = ['amount', 'listing_id']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        listing_id = self.cleaned_data.get('listing_id')
        listing = get_object_or_404(Listing, id=listing_id)
        if amount <= listing.current_bid:
            raise forms.ValidationError(f'Your bid must be higher than the current bid of ${listing.current_bid}')
        return amount


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }
