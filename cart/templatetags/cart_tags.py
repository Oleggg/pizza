from django.template.base import Library

from django import template

from cart.models import Cart
from cart.views import get_session_cart
from cart.views import get_cart

#register = Library()
register = template.Library()
#template = 'shop/templatetags/_cart.html'
@register.inclusion_tag('templatestags/cart_tag.html', takes_context=True)
#@register.inclusion_tag('cart_tag.html', takes_context=True)
def cart_info(context):
    #print 'CALLED cart_tag'
    #print context
    #session = getattr(request, 'session', None)
    #print 'SESSION: '
    #print session['CART_ID']
    request = context['request']
    #print request.session['CART_ID']
    cart = get_session_cart(context['request'])
    #cart = get_cart(context['request'])
    return {'cart_object': cart}

"""class Cart(InclusionTag):
    #template = 'shop/templatetags/_cart.html'

    def get_context(self, context):
        #cart = get_or_create_cart(context['request'])
        cart = get_session_cart(context['request'])
        #cart.update()
        return {
            'cart': cart
        }
register.tag(Cart)"""

