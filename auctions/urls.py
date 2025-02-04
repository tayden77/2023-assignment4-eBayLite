from django.urls import path
from .views import ListingUpdateView, ListingDeleteView, CloseBiddingView
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
    path("listing/<int:pk>/place_bid/", views.place_bid, name="place-bid"),
    path("listing/<int:pk>/close_bid/", CloseBiddingView.as_view(), name="close-bidding"),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path('listing/<int:pk>/add_to_watchlist/', views.add_to_watchlist, name='add-to-watchlist'),
    path('listing/<int:pk>/remove_from_watchlist/', views.remove_from_watchlist, name='remove-from-watchlist'),
    path('category/<int:category_id>/', views.category_detail_view, name='category-detail'),
    path('listing/<int:pk>/comment/', views.create_comment, name='create-comment')
]
