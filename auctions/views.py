from typing import Any
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from .models import User, Listing, Category, Bid, Watchlist, Comment
from .forms import ListingForm, BidForm, CommentForm

# Index page view
def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {'listings': listings})

# Views to update and delete existing listings
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

# Views to place bids and close bidding on user owned items
@login_required
def place_bid(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.listing = listing
            if bid.amount > listing.current_bid:
                listing.current_bid = bid.amount
                listing.save()
                bid.save()
                return redirect('listing-detail', pk=pk)
            else:
                form.add_error('amount', 'Bid must be higher than the current bid')
    else:
        form = BidForm()
    return render(request, 'auctions/place_bid.html', {'form': form, 'listing': listing})        

class CloseBiddingView(View):
    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        if not request.user.is_authenticated or request.user != listing.creator:
            messages.error(request, 'You are not authorized. Please create an account or log-in.')
            return redirect('listing-detail', pk=listing.id)
        listing.is_active = False
        listing.save()
        return redirect('listing-detail', pk=listing.id)
    
# Views to add and remove listings to and from the watchlist as well as load user's watchlist
@login_required    
def watchlist_view(request):
    user = request.user
    try:
        watchlist = Watchlist.objects.get(user=user)
        watchlist_items = watchlist.listings.all()
    except Watchlist.DoesNotExist:
        watchlist_items = []
    return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})

@login_required
def add_to_watchlist(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listings.add(listing)
    return redirect('listing-detail', pk=pk)

@login_required
def remove_from_watchlist(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    if not created:
        watchlist.listings.remove(listing)
    return redirect('listing-detail', pk=pk)

# View to access detailed category page
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, 'auctions/category_detail.html', {'category': category, 'listings': listings})

# Login, Logout, and Register views
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
    
# Views to create listings and view a detailed listing page    
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
    listing = get_object_or_404(Listing, pk=pk)
    comments = Comment.objects.filter(listing=listing)
    bids = Bid.objects.filter(listing=listing).order_by('-timestamp')
    bid_form = BidForm()
    comment_form = CommentForm()  # initialize comment form

    if request.method == "POST" and 'submit_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
            return redirect('listing-detail', pk=pk)

    context = {
        'listing': listing,
        'bid_form': bid_form,
        'bids': bids,  # pass bids to template
        'comments': comments,
        'comment_form': comment_form  # pass comment form to template
    }
    return render(request, 'auctions/listing_detail.html', context)

# View to create a comment on a listing
@login_required
def create_comment(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = get_object_or_404(Listing, id=pk)
            comment.user = request.user
            comment.save()
            return redirect('listing-detail', pk=pk)
        else:
            return render(request, 'auctions/comment.html', {'form': form, 'listing_id': pk})
    else:
        form = CommentForm()
        return render(request, 'auctions/comment.html', {'form': form, 'listing_id': pk})