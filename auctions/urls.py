from django.urls import path
from .views import ListingUpdateView, ListingDeleteView, PlaceBidView, CloseBiddingView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create-listing"),
    path("listing/<int:pk>/edit/", ListingUpdateView.as_view(), name="listing-edit"),
    path("listing/<int:pk>/delete/", ListingDeleteView.as_view(), name="listing-delete"),  
    path("listing/<int:pk>", views.listing_detail, name="listing-detail"),
    path("listing/<int:pk>/bid/", PlaceBidView.as_view(), name="place-bid"),
    path("listing/<int:pk>/close_bid/", CloseBiddingView.as_view(), name="close-bidding")
]
