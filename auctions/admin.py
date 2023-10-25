from django.contrib import admin
from .models import User, Listing, Bid, Comment, Category, Watchlist

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)
