from django.shortcuts import redirect, render
from home.models import *
from .models import Wishlist
from home.views import BaseView
from django.contrib.auth.decorators import login_required


# Create your views here.
# -----------------Wishlist----------------------
@login_required
def add_to_wishlist(request, slug):
    username = request.user.username

    data = Wishlist.objects.create(
        username=username,
        items=Item.objects.filter(slug=slug)[0],
        slug=slug
    )
    data.save()
    return redirect('wishlist:my_wishlist')


class WishlistView(BaseView):
    def get(self, request):
        username = request.user.username
        self.views['my_wishlist'] = Wishlist.objects.filter(username=username, checkout=False, )
        return render(request, 'wishlist.html', self.views)


def delete_wishlist(request, slug):
    username = request.user.username
    Wishlist.objects.filter(username=username, checkout=False, slug=slug).delete()
    return redirect('wishlist:my_wishlist')
