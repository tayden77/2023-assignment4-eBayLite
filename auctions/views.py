from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User, Listing, Category, Bid
from .forms import ListingForm, BidForm
import logging

def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {'listings': listings})


class ListingUpdateView(UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'auctions/listing_edit.html'
    context_object_name = 'listing'

    def get_success_url(self):
        return reverse_lazy('listing-detail', kwargs={'pk': self.object.pk})
    
    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)
    

class ListingDeleteView(DeleteView):
    model = Listing
    template_name = 'auctions/listing_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('index')    

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user) 
    

class PlaceBidView(View):
    def post(self, request, pk):
        logging.info(f'Listing ID: {pk}')
        listing = get_object_or_404(Listing, id=pk)
        if not listing.is_active:
                messages.error(request, 'Bidding on this item is closed')
                print(form.errors)
                return redirect('listing-detail', pk=listing.id)
        form = BidForm(request.POST, initial={'listing_id': pk})
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.user = request.user
            bid.save()
            return redirect('place-bid', pk=listing.id)
        else:
            messages.error(request, 'There was a problem with your bid entry. Please try again')
            
            return render(request, 'listing_detail.html', {'form': form})
        

class CloseBiddingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(Listing, id=pk)
        if not request.user.is_authenticated or request.user != listing.creator:
            messages.error(request, 'You are not authorized. Please create an account or log-in.')
            return redirect('listing-detail', pk=listing.id)
        listing.is_active = False
        listing.save()
        return redirect('listing-detail', pk=listing.id)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.current_bid = listing.starting_bid
            listing.save()
            return redirect('index')
        else: 
            print(form.errors)
            return render(request, 'auctions/create_listing.html', {'form':form, 'form_errors':form.errors})
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, id=pk)
    bid_form = BidForm()
    return render(request, 'auctions/listing_detail.html', {'listing': listing, 'bid_form': bid_form})