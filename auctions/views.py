from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import ListingForm
from .models import Listing, Category
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {'listings': listings})


class ListingUpdateView(UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = 'auctions/listing_edit.html'
    context_object_name = 'listing'

    def get_success_url(self):
        return reverse_lazy('listing-detail', kwargs={'listing_id': self.object.pk})
    
    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)
    

class ListingDeleteView(DeleteView):
    model = Listing
    template_name = 'auctions/listing_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('index')    

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user) 


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
            return render(request, 'auctions/create_listing.html', {'from':form, 'form_errors':form.errors})
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    return render(request, 'auctions/listing_detail.html', {'listing': listing})