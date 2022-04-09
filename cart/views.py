from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.shortcuts import render
from home.models import *
from .models import Cart, Contact, Checkout
from home.views import BaseView
from django.contrib.auth.decorators import login_required


# --------------Cart-------------------
@login_required
def add_to_cart(request, slug, totals=None):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).discounted_price

    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price

    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        quantity = quantity + 1
        total = original_price * quantity
        totals = total + total
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(quantity=quantity, total=total, totals=totals)
        return redirect('cart:my_cart')
    else:
        quantity = 1

    total = original_price * quantity
    totals = total + total
    data = Cart.objects.create(
        username=username,
        items=Item.objects.filter(slug=slug)[0],
        slug=slug,
        quantity=quantity,
        total=total,
        totals=totals,
    )

    data.save()
    return redirect('cart:my_cart')


def delete_one(request, slug):
    username = request.user.username
    totals = Item.objects.get(slug=slug).totals
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).discounted_price
    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price

    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        quantity = quantity - 1
        total = original_price * quantity
        totals = totals + total
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(quantity=quantity, total=total, totals=totals)
        return redirect('cart:my_cart')
    else:
        quantity = 1
        totals = original_price
    total = original_price * quantity
    totals = totals + total
    data = Cart.objects.create(
        username=username,
        items=Item.objects.filter(slug=slug),
        slug=slug,
        quantity=quantity,
        total=total,
        totals=totals,
    )

    data.save()
    return redirect('cart:my_cart')


class CartView(BaseView):
    def get(self, request):
        username = request.user.username
        self.views['my_cart'] = Cart.objects.filter(username=username, checkout=False, )
        return render(request, 'cart.html', self.views)


def delete_cart(request, slug):
    username = request.user.username
    Cart.objects.filter(username=username, checkout=False, slug=slug).delete()
    return redirect('cart:my_cart')


@login_required()
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
        messages.success(request, 'Your Message has been sent.')

        # email = EmailMessage(
        #     f'Hello {name}\n{email}',
        #     f'subject:{subject}\n{message}',
        #     'r1ka1@gmail.com',
        #     ['7mmmm4n7@gmail.com'],
        # )
        # email.send()

    else:
        messages.error(request, 'Your Message has not been sent.')

    return render(request, 'contact.html')


@login_required()
def checkout(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        address = request.POST['address']
        zip_code = request.POST['zip_code']
        phone = request.POST['phone']
        checkout = Checkout.objects.create(
            f_name=f_name,
            l_name=l_name,
            email=email,
            address=address,
            zip_code=zip_code,
            phone=phone,
        )
        checkout.save()
        messages.success(request, 'Your Checkout has been REGISTERED.')
    return render(request, 'checkout.html')
