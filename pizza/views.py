#coding: utf-8
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import ListView, CreateView
from .models import Pizza, Order, Deliveryman
from django.http import Http404
from django import forms
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse_lazy
from .forms import OrderForm

from pizza.models import OrderItem
from pizza.forms import OrderItemFormset
from pizza.forms import OrderFromCartForm
from pizza.forms import get_order_formset
from pizza.forms import get_order_from_cart_formset
from cart.models import Cart
from cart.views import get_session_cart

class PizzaListView(ListView):
    model = Pizza
    template_name = 'index.html'
    template_context_name = 'pizza_list'

pizza_list = PizzaListView.as_view()

class MargaritaPizzaListView(PizzaListView):
    def get_queryset(self):
        return super(MargaritaPizzaListView, self).get_queryset().filter(name__icontains = 'аргарита')

margo = MargaritaPizzaListView.as_view()

class CreateOrderView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order.html'
    success_url = reverse_lazy('home')

    def get(self, request, **kwargs):
        print '### CALLED GET ###'
        #self.object = User.objects.get(username=self.request.user)
        cart = get_session_cart(self.request)
        print '############ CART ###########'
        print cart
        if cart:
            order = create_from_cart(cart)
            print '############ ORDER ###########'
            print order
            self.object = order
        else:
            self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    #def get(self, request, **kwargs):
        #self.object = User.objects.get(username=self.request.user)
        #form_class = self.get_form_class()
        #form = self.get_form(form_class)
        #context = self.get_context_data()
        #return self.render_to_response(context)

    #def get_initial(self):
    #    print 'CALLED get_initial' 
        # Get the initial dictionary from the superclass method
    #    initial = super(CreateOrderView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
    #    initial = initial.copy()
        #cart = get_object_or_404(Cart, pk=self.kwargs[u'pk'])
        #initial['user'] = self.request.user.pk
           # etc...
    #    return initial

    """def get_object(self, queryset=None):
        print 'CALLED GET_object'
        cart = get_session_cart(self.request)
        print '############ CART ###########'
        print cart
        order = create_from_cart(cart)
        print '############ ORDER ###########'
        print order
        return order"""

    """def get_form(self, form_class):
        print 'CALLED get_form'
        form_class = self.get_form_class()
        #print form_class
        form = super(CreateOrderView, self).get_form(form_class)
        #course = get_object_or_404(Class, pk=self.kwargs['pk'])
        #cart = get_object_or_404(Cart, pk=self.kwargs['pk'])
        cart = get_session_cart(self.request)
        print '############ CART ###########'
        print cart
        order = create_from_cart(cart)
        print '############ ORDER ###########'
        print order
        #form.instance.course = course
        form.instance.order = order
        return form"""

    def get_context_data(self, *args, **kwargs):
        context_data = super(CreateOrderView, self).get_context_data(*args, **kwargs)
        #context_data.update({'order': self.order})
        #print "||||||||||||||| SELF.object ||| "
        #print self.object.orderitem_set.all()
        if self.object:
            context_data['formset'] = get_order_formset(items=self.object.orderitem_set.all())
        else:
            context_data['formset'] = OrderItemFormset()
        print "||||||||||||||| SELF.object ||| "
        print context_data['formset'] 
        return context_data

    """def post(self, request, **kwargs):
        return http.HttpResponse("Post")"""

    def get_form_kwargs(self):
        kwargs = super(CreateOrderView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        if form.is_valid() and form.formset.is_valid():
            self.object = form.save()
            form.formset.instance = self.object
            form.formset.save()
            return HttpResponseRedirect(self.get_success_url()) 
        else:
            return self.form_invalid(form)
            #return self.render_to_response(self.get_context_data())

create_order = CreateOrderView.as_view()

#def create_from_cart(self, request):
def create_from_cart(cart):
    #cart = get_session_cart(request)
    #order = self.model()
    order = Order()
    order.cost = cart.total
    #order.address = 'Sample address'
    order.save()
    for cart_item in cart.items.all():
        oitem = OrderItem()
        oitem.pizza = cart_item.product
        oitem.quantity = cart_item.quantity
        oitem.order = order
        oitem.save()
    return order

# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.info(request, form.cleaned_data['comment'])
#             return redirect('home')
#         else:
#             return TemplateResponse(request, 'order.html', {'form': form})
#         #handle form
#     elif request.method == 'GET':
#         form = OrderForm()
#         return TemplateResponse(request, 'order.html', {'form': form})
#     else:
#         raise Http404
        

class CreateOrderFromCartView(CreateView):

    template_name = 'cart_order.html'
    form_class = OrderFromCartForm
    model = Order

    #def get(self, request, **kwargs):
    #    self.object = Cart.objects.get(pk=self.kwargs['pk'])
    #    form_class = self.get_form_class()
    #    form = self.get_form(form_class)
    #    context = self.get_context_data(object=self.object, form=form)
    #    return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        #cart = Cart.objects.get(pk=self.kwargs['pk'])
        context = super(CreateOrderFromCartView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['order_formset'] = get_order_from_cart_formset(self.request.POST, items=None)
        else:
            context['order_formset'] = get_order_from_cart_formset()
        return context

create_order_cart = CreateOrderFromCartView.as_view()
