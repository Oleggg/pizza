#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Order, Deliveryman, OrderItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.models import inlineformset_factory
OrderItemFormset = inlineformset_factory(Order, OrderItem, extra=2)

class CreateOrderForm(forms.Form):
    comment = forms.CharField(label = 'Comment')

class OrderForm(forms.ModelForm):
    comment = forms.CharField(label = 'Comment', required=False,
        widget = forms.Textarea(attrs={'cols':'10', 'rows':'10'}))
    class Meta:
        model = Order
        fields = ('city', 'address', )

    def __init__(self, request, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'Order'
        self.helper.add_input(Submit('', 'Submit'))
        if request.method == 'POST':
            self.formset = OrderItemFormset(request.POST)
        else:
            self.formset = OrderItemFormset()
        #    self.formset = self.context['formset']

    def save(self, *args, **kwargs):
        self.instance.deliveryman = Deliveryman.objects.get(name = 'user1')
        return super(OrderForm, self).save(*args, **kwargs)

    def clean(self):
        if self.cleaned_data['city'] == Order.PENZA and \
            not self.cleaned_data['address'].strip():
            raise forms.ValidationError('Please fill in address')
        return self.cleaned_data

def get_order_formset(items=None):
    #CartFormSet = inlineformset_factory(Cart, CartItem, extra=1)
    #CartFormSet = inlineformset_factory(Cart, CartItem, extra=len(items))

    #OrderItemFormset = modelformset_factory(CartItem, form=CartItemForm, extra=0)
    OrderItemFormset = inlineformset_factory(Order, OrderItem, extra=0)

    #CartFormSet = inlineformset_factory(Cart, CartItem, form=CartItemForm, extra=0)
    #CartFormSet = inlineformset_factory(CartForm, CartItem, extra=2)
    if items:
        print '||||||||||||||| WITH ITEMS '
        kwargs = {'queryset': items, }
        print items.values()
        #order_formset = OrderItemFormset(data, **kwargs)

        #order_formset = OrderItemFormset(**kwargs)
        order_formset = OrderItemFormset(initial = items)

        #order_formset = OrderItemFormset()
        #for form, data in zip(order_formset.forms, **kwargs):
        #    form.initial = data
    else:
        print '############ WITHOUT ITEMS '
        order_formset = OrderItemFormset()
    for form in order_formset:
        print '||||||||||||||||||| form.instance.pk '
        print form.instance.pk
        for item in items:
            print '||||||||||||||||||| ITEM PK '
            print item.pk
            print '||||||||||||||||||| ITEM QUANTITY '
            print item.quantity
            if form.instance.pk == item.pk:
                #data = {'id': item.pk, 'quantity': item.quantity}
                form.instance = item
                #form.initial = data
                #form.initial = item
    return order_formset
