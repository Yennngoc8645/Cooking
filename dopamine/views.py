from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
     products = Product.objects.all()
     context= {'products': products}
     return render(request,'dopamine/home.html', context)
def cart(request):
    context= {}
    return render(request, 'dopamine/cart.html', context)
def checkout(request):
    context= {}
    return render(request,'dopamine/checkout.html', context)



