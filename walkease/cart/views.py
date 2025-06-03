from django.shortcuts import render

from django.http import HttpResponse

def cart_view(request):
    return HttpResponse("This is the cart page.")