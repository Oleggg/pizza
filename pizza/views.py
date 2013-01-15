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
        cart = get_session_cart(self.request)
        if cart:
            order = create_from_cart(cart)
            self.object = order
        else:
            self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context_data = super(CreateOrderView, self).get_context_data(*args, **kwargs)
        if self.object:
            context_data['formset'] = get_order_formset(items=self.object.orderitem_set.all())
        else:
            context_data['formset'] = OrderItemFormset()
        return context_data

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

def create_from_cart(cart):
    order = Order()
    order.cost = cart.total
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

    def get_context_data(self, **kwargs):
        #cart = Cart.objects.get(pk=self.kwargs['pk'])
        context = super(CreateOrderFromCartView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['order_formset'] = get_order_from_cart_formset(self.request.POST, items=None)
        else:
            context['order_formset'] = get_order_from_cart_formset()
        return context

create_order_cart = CreateOrderFromCartView.as_view()
