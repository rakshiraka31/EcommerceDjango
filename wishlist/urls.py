from django.urls import path
from .views import *
app_name = 'wishlist'

urlpatterns = [
    path('add-to-wishlist/<slug>', add_to_wishlist, name='add-to-wishlist'),
    path('my_wishlist', WishlistView.as_view(), name='my_wishlist'),
    path('delete_wishlist/<slug>', delete_wishlist, name='delete_wishlist'),
]