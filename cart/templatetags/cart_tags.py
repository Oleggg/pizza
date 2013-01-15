from django.template.base import Library

from django import template

from cart.models import Cart
from cart.views import get_session_cart
from cart.views import get_cart

#register = Library()
register = template.Library()
@register.inclusion_tag('templatestags/cart_tag.html', takes_context=True)
#@register.inclusion_tag('cart_tag.html', takes_context=True)
def cart_info(context):
    cart = get_session_cart(context['request'])
    #cart = get_cart(context['request'])
    return {'cart_object': cart}


