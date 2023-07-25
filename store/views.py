from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib import messages
from  .models import Product,Cart,CartProduct
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'login.html',  messages.error(request,"login failed"))
    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login') 


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_products = cart.cartproduct_set.all()

    return render(request, 'cart.html', {'cart': cart, 'cart_products': cart_products})
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product already exists in the user's cart
    cart_product, _ = CartProduct.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If the product already exists, increment the quantity
        cart_product.quantity += 1
        cart_product.save()

    return redirect('cart')
@login_required
def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    cart_product.delete()

    return redirect('cart')
@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartproduct_set.all().delete()
    
    return redirect('cart')


def subtotal(request):
    cart = Cart.objects.get(user=request.user)
    cart_products = cart.cart_product_set.all()
    subtotal = sum(cart_product.quantity * cart_product.product.price for cart_product in cart_products)
    return render(request, 'subtotal.html', {'subtotal': subtotal})



