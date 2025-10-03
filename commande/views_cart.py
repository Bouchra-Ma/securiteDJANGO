# commande/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, "commande/cart_detail.html", {"cart": cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect("cart_detail")

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")
