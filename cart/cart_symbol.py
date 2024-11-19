
from .models import Cart, Cartitem
from industry.views import _cart_id
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            # Fetch the cart for the authenticated user
            cart = Cart.objects.get(cart_id=request.user.email)
            cart_items = Cartitem.objects.filter(cart=cart)
        else:
            # Handle the case for an anonymous user using the session-based cart ID
            cart_id = _cart_id(request)  # Use session-based cart_id for anonymous users
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = Cartitem.objects.filter(cart=cart)

        # Sum up the quantity of items in the cart
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except (Cart.DoesNotExist, Cartitem.DoesNotExist):
        cart_count = 0

    return dict(cart_count=cart_count)
