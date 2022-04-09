from django.contrib import admin
from django.urls import path
from .views import *
app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryItemView.as_view(), name='category'),
    path('product_detail/<slug>', ItemDetailView.as_view(), name='product_detail'),
    path('product_list', ItemListView.as_view(), name='product_list'),
    path('product_list2', ItemList2View.as_view(), name='product_list2'),
    path('search', ItemSearchView.as_view(), name='search'),
    path('contact', ContactFormView.as_view(), name='contact'),
    path('account', AccountView.as_view(), name='account'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('api_data', api_data, name='api_data')

]
