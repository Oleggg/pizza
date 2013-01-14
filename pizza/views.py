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

from cart.models import Cart

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

    #################################
    def get_initial(self):
        print 'CALLED get_initial' 
        # Get the initial dictionary from the superclass method
        initial = super(CreateOrderView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
    #    initial = initial.copy()
        #cart = get_object_or_404(Cart, pk=self.kwargs[u'pk'])
        #initial['user'] = self.request.user.pk
           # etc...
        return initial

    """def get_form(self, form_class):
        print 'CALLED get_form'
        form_class = self.get_form_class()
        print form_class
        form = super(CreateOrderView, self).get_form(form_class)
        #course = get_object_or_404(Class, pk=self.kwargs['pk'])
        #cart = get_object_or_404(Cart, pk=self.kwargs['pk'])
        #print '############ CART ###########'
        #print cart
        #form.instance.course = course
        return form"""
    """def post(self, request, **kwargs):
        return http.HttpResponse("Post")

    def get_form_kwargs(self):
        kwargs = super(CreateOrderView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs"""

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
        
