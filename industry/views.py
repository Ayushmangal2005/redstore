from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect,  get_object_or_404
from django.db import models
from django.core.mail import send_mail

from django.conf import settings

from items.models import Product
from cart.models import Contact

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

from cart.models import Cart, Cartitem
import uuid
import requests

grand_total=0


def productview(request, myid):
    product = Product.objects.get(number=myid)
    print(product.number)

    return render(request, "product_detail.html", {'product': product})


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'].strip()
        if keyword:

            try:
                product = Product.objects.get(product_name=keyword)
                print(product)
                return render(request, "product_detail.html", {'product': product})


            except Product.DoesNotExist:
                return render(request, "product_detail.html", {'error': f'No products found for "{keyword}".'})

    return render(request, "product_detail.html", {'error': 'Please enter a search term.'})






def generate_unique_cart_id():
    return str(uuid.uuid4())








def home(request):
    return render(request, "index.html")

def index(request):
    return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")





def productdisplay(request, categories):
    products = Product.objects.filter(category=categories)
    catprods = Product.objects.filter(category=categories).values('product_name', 'price', 'id', 'image', 'number', 'category')

    params={'allprods': catprods , 'category':categories}

    return render(request, "product_display.html", params)








def remove_cart(request, product_number):
    cart_id = request.user.email

    cart = Cart.objects.get(cart_id=cart_id)
    product = get_object_or_404(Product, number = product_number)

    try:

         cart_item = Cartitem.objects.get(product=product , cart=cart)

         if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
         else:
            cart_item.delete()

    except Cartitem.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart_item(request, product_number):
    cart_id = request.user.email
    cart= Cart.objects.get(cart_id=cart_id)
    product = get_object_or_404(Product,  number=product_number)
    try:
        cart_item= Cartitem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except Cartitem.DoesNotExist:
        pass

    return redirect('cart')


def placeorder(request):

    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    Email = request.session.get('Email')
    number = request.session.get('number')
    address = request.session.get('address')


    subject="test mail"

    if first_name and number and address and Email and last_name:
      message = (
        f"We have received your orders.\n"
        f"First Name: {first_name}\n"
        f"Last Name: {last_name}\n"
        f"Email: {Email}\n"
        f"Number: {number}\n"
        f"Address: {address}"
      )
      from_email = settings.EMAIL_HOST_USER
      recipient_list =[Email]
      send_mail(subject,message,from_email,recipient_list)


      return render(request, "index.html")

    else:
        return redirect('checkout')







def checkout(request, total=0, quantity=0, cart_items=None):

    if request.user.is_authenticated:

      try:
        cart_id=request.user.email
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100

        discount = request.session.get('discount', 0)

        grand_total = total + tax - discount

        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            number = request.POST.get('phone')
            address = request.POST.get('address')

            print(first_name)
            print(last_name)
            print(email)
            print(number)
            print(address)

            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=number,
                address=address
            )


            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['Email'] = email
            request.session['number'] = number
            request.session['address'] = address









      except ObjectDoesNotExist:
        return render(request, "cart.html")

    grand_total = request.session.get('grand_total')



    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,


        'grand_total': grand_total

    }



    return render(request, "checkout.html", context)





def cart(request, total=0, quantity=0, cart_items=None):
    cart_items = []
    tax = 0
    grand_total = 0

    discount = 0
    message=""


    if request.user.is_authenticated:
        try:
            cart_id = request.user.email  # or another identifier
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = Cartitem.objects.filter(cart=cart, is_active=True)



            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax



            if request.method == "POST":
                coupon_code = request.POST.get('coupon')
                if coupon_code == "diwali":
                    discount = (20 * (grand_total)) / 100
                    request.session['discount'] = discount
                    grand_total = grand_total - discount
                    message = "coupon applied"

                else:
                    message = "invalid coupon code"




        except ObjectDoesNotExist:
            # Handle case where cart or cart items don't exist
            return render(request, "cart.html", {'message': 'Your cart is empty or does not exist.'})

    else:
        # Handle case for anonymous users (optional)
        return render(request, "cart.html", {'message': 'Your cart is empty or does not exist.'})
    request.session['grand_total'] = grand_total
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'message': message
    }

    return render(request, "cart.html", context)























@login_required(login_url="login")
def add_cart(request, product_number):

    product = Product.objects.get(number=product_number)
    print(product)
    cart_id=request.user.email
    print(cart_id)


    try:
      cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
      cart = Cart.objects.create(
            cart_id=cart_id
      )
    cart.save()

    try:
        cart_item = Cartitem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()

    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    return redirect('cart')


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




def loginaction(request):
    global email
    if request.method == "POST":
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.filter(username=email)


        if not user.exists():
            return render(request, "login.html", {'error': 'Account not found'})

        user = authenticate(username=email, password=password)

        if user:
            try:
                cart_id=request.user.email

                cart = Cart.objects.get_or_create(cart_id=cart_id)


                is_cart_items_exists = Cartitem.objects.filter(cart=cart).exists()


                if is_cart_items_exists:

                  cart_item = Cartitem.objects.filter(cart=cart)


                  for item in cart_item:
                        item.user = user
                        item.save()

            except Exception as e:
                print(f"Exception occurred: {e}")

            login(request , user)

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
            except:
                return redirect('home')








        return render(request, "login.html", {'error': 'Invalid email or password'})

    return render(request, "login.html")

def signaction(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.filter(username=email)


        if user.exists():
           return render(request, "register.html", {'error': 'email already taken'})

        if not first_name:
            return render(request, "register.html", {'error': 'First name is required'})

        user = User.objects.create_user(first_name=first_name , password=password , email=email, username = email)



        return render(request, "register.html", {'error': 'You Have Successfully Registered'})



    return render(request, "register.html")


@login_required(login_url="login")
def logoutuser(request):
    logout(request)
    return render(request, "index.html")