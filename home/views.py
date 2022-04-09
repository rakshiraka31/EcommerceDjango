import json
import requests
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from django.contrib.auth import authenticate, login


# Create your views here.
class BaseView(View):
    views = {}
    views['category'] = Category.objects.filter(status='active')


class HomeView(BaseView):
    def get(self, request):
        self.views['sliders'] = Slider.objects.filter(status='active')
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.filter(status='active')
        self.views['hots'] = Item.objects.filter(status='active', label='hot')
        self.views['news'] = Item.objects.filter(status='active', label='new')
        self.views['reviews'] = Review.objects.filter(status='active')

        return render(request, 'index.html', self.views)


class CategoryItemView(BaseView):
    def get(self, request, slug):
        category_id = Category.objects.get(slug=slug).id
        self.views['cat_items'] = Item.objects.filter(category=category_id)
        return render(request, 'category.html', self.views)


class BrandItemView(BaseView):
    def get(self, request, slug):
        brand_id = Brand.objects.get(slug=slug).id
        self.views['brand_items'] = Item.objects.filter(brand=brand_id)
        return render(request, 'brand.html', self.views)


class ItemSearchView(BaseView):
    def get(self, request):
        search = request.GET.get('search', None)
        if search is None:
            return redirect('/')
        else:
            self.views['search_items'] = Item.objects.filter(name__icontains=search)
            return render(request, 'search.html', self.views)

        return render(request, 'search.html')


class ItemDetailView(BaseView):
    def get(self, request, slug):
        self.views['product_details'] = Item.objects.filter(slug=slug)
        return render(request, 'product-detail.html', self.views)


class ItemListView(BaseView):
    def get(self, request):
        self.views['product_list'] = Item.objects.filter()
        return render(request, 'product-list.html', self.views)


class ItemList2View(BaseView):
    def get(self, request):
        self.views['product_list2'] = Item.objects.filter()
        return render(request, 'product-list2.html', self.views)


class AccountView(BaseView):
    def get(self, request):
        self.views['account'] = Item.objects.filter()
        return render(request, 'my-account.html', self.views)


class ContactFormView(BaseView):
    def get(self, request):
        self.views['contact'] = Item.objects.filter()
        return render(request, 'contact.html', self.views)


def signup(request):
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return redirect('home:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already taken.')
                return redirect('home:signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=f_name,
                    last_name=l_name
                )
                user.save()
                messages.success(request, 'Your account has been registered.')
                return redirect('home:signup')
        else:
            messages.error(request, 'The passwords do not match.')
            return redirect('home:signup')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username/Password doesnt match.')
            return redirect('home:login')

    return render(request, 'login.html')


# ------------------------API------------------------------


from .models import *
from .serializers import *
from rest_framework import generics, status, viewsets, serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response


# ViewSets define the view behavior.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class FilterItemViewSet(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_fields = ['id', 'category', 'label']
    ordering_filter = ['id', 'price', 'title']
    search_fields = ['title', 'description']


class ItemDetail(APIView):

    def get_object(self, pk):
        try:
            return Item.objects.get(id=pk)
        except:
            raise Http404

    def get(self, request, pk):
        object = self.get_object(pk)
        serializers = ItemSerializer(object)
        return Response(serializers.data)

    def put(self, request, pk):
        object = self.get_object(pk)
        serializers = ItemSerializer(object, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            pass
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        object = self.get_object(pk)
        object.delete()

        return Response("The row is deleted.", status=status.HTTP_200_OK)


def api_data(request):
    api_url = "http://127.0.0.1:8000/api/items/"
    response = requests.get(api_url)
    records = response.text
    records = json.loads(records)
    return render(request, 'api.html', {'items': records})
