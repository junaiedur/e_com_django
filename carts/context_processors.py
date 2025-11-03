# from .models import Cart, CartItem
# from .views import _cart_id

# # def counter(request):
# #     cart_count = 0
# #     if 'admin' in request.path:
# #         return{}
# #     else:
# #         try:
# #             cart = Cart.objects.filter(cart_id=_cart_id(request))
# #             if request.user.is_authenticated:
# #                 cart_items = CartItem.objects.all().filter(user=request.user)
# #             else:
                
# #                 cart_items = CartItem.objects.all().filter(cart=cart[:1])
# #             for cart_item in cart_items:
# #                 cart_count += cart_item.quantity
# #         except Cart.DoesNotExist:
# #             cart_count = 0
# #     return dict(cart_count=cart_count)


# ###ai line ta deep seek teke neya:


# def counter(request):
#     cart_count = 0
#     if 'admin' in request.path:
#         return {}
#     else:
#         # Attempt to retrieve cart items based on user authentication
#         try:
#             cart = Cart.objects.filter(cart_id=_cart_id(request))
#             if request.user.is_authenticated:
#                 cart_items = CartItem.objects.filter(user=request.user, is_active=True)
#             else:
#                 #cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
#                 cart_items = CartItem.objects.all().filter(cart=cart[:1])

#                 #cart_items = CartItem.objects.filter(cart=cart, is_active=True) if cart else []
#             for cart_item in cart_items:
#                 cart_count += cart_item.quantity
#             #cart_count = sum(cart_item.quantity for cart_item in cart_items)
#         except Cart.DoesNotExist:
#             cart_count = 0
            
#         return {'cart_count': cart_count}
#         #return dict(cart_count=cart_count)



# new in deepseek

from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
                if cart:
                    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                else:
                    cart_items = []
            
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
            
    return {'cart_count': cart_count}