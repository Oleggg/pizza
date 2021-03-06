# Create your views here.
#coding: utf-8
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.views.generic import View
from django.views.generic import UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils import simplejson as json
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from pizza.models import Pizza
from cart.models import Cart
from cart.forms import get_cart_formset
from cart.forms import CartForm
from cart.forms import CartItemForm

from decimal import Decimal

#class CartDetailView(View):
#template_name = 'cart.html'


class CartUpdateView(UpdateView):

    template_name = 'cart/edit.html'
    form_class = CartForm
    model = Cart

    def get(self, request, **kwargs):
        #self.object = User.objects.get(username=self.request.user)
        self.object = Cart.objects.get(pk=self.kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        #context = super(CartUpdateView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(pk=self.kwargs['pk'])
        context = super(CartUpdateView, self).get_context_data(**kwargs)
        #context = super(CartUpdateView, self).get_context_data(cart_items=cart.items)
        if self.request.POST:
            context['cart_formset'] = get_cart_formset(self.request.POST, items=cart.items.all())
        else:
            context['cart_formset'] = get_cart_formset(items=cart.items.all())
        return context

    def get_object(self, queryset=None):
        obj = Cart.objects.get(pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        context = self.get_context_data()
        cart_form = context['cart_formset']
        if cart_form.is_valid():
            self.object = form.save()
            cart_form.instance = self.object
            cart_form.save()
            return HttpResponseRedirect('/cart/edit/' + str(form.instance.pk))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

edit = CartUpdateView.as_view()

#def cart(self, request, *args, **kwargs):
def cart(request):
    cart = get_cart(request)
    return render_to_response("cart/cart.html", {'cart': cart} )
    #return render_to_response("cart/cart.html", {'cart': cart}, context_instance=RequestContext(request) )
    #return render_to_response("cart/cart.html", {'cart': cart, 'RequestContext': RequestContext(request) }, context_instance=RequestContext(request) )

def edit(request):
    self.formset = OrderItemFormset()
    return render_to_response("cart/edit.html", {'cart': cart} )

def add_product(request, *args, **kwargs):
    cart = get_cart(request)
    #cart.save()
    pizza_id = request.POST['add_pizza_id']
    quantity = request.POST['quantity']
    pizza = Pizza.objects.get(pk=pizza_id)
    cart.add_cart_item(pizza,quantity)
    #return HttpResponse(json.dumps("success"), mimetype="application/json")
    #return HttpResponse("success", mimetype="text/html")
    #'total_cost': cost + u' руб',
    #cost = json.dumps(Decimal(cart.total), use_decimal=True)
    cost = json.dumps(Decimal(cart.total), cls=DjangoJSONEncoder)
    data = json.dumps({
        'quantity': cart.count,
        #'total_cost': cost,
        'total_cost': str(cart.total)
    })
    return HttpResponse(data, content_type='application/json')

def get_session_cart(request):
    cart = None
    session = getattr(request, 'session', None)
    cid = session.get('CART_ID')
    if cid:
        cart = Cart.objects.get(pk = cid)
    return cart

def get_cart(request):
    cart = get_session_cart(request)
    if not cart:
        cart = Cart()
        cart.save()
        request.session['CART_ID'] = cart.pk
        #print cart.pk
    return cart

def clear_cart(request):
    session = getattr(request, 'session', None)
    cart = get_session_cart(request)
    if cart:
        cart.clear()
        request.session['CART_ID'] = None
    return render_to_response("cart/cart.html", {'cart': cart} )
