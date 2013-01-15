#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django import forms
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory

from cart.models import Cart
from cart.models import CartItem

class CartForm(forms.ModelForm):

    #total = forms.CharField(label = 'Total cost', required=True )
    created_date = forms.CharField(label = 'Date', required=False )

    class Meta:
        model = Cart
        fields = ('created_date', )

    def save(self, *args, **kwargs):
        return super(CartForm, self).save(*args, **kwargs)

class CartItemForm(forms.ModelForm):

    #pk = forms.CharField(label = 'PK', required=True )
    quantity = forms.IntegerField(label = u'Количество', required=False )

    class Meta:
        model = CartItem
        fields = ( 'quantity', )
        #fields = ('pk', 'quantity', )

    def save(self, *args, **kwargs):
        return super(CartItemForm, self).save(*args, **kwargs)

#def get_cart_formset(items=None, data=None):
def get_cart_formset( data=None, items=None):
    #CartFormSet = inlineformset_factory(Cart, CartItem, extra=1)
    #CartFormSet = inlineformset_factory(Cart, CartItem, extra=len(items))

    CartFormSet = modelformset_factory(CartItem, form=CartItemForm, extra=0)

    #CartFormSet = inlineformset_factory(Cart, CartItem, form=CartItemForm, extra=0)
    #CartFormSet = inlineformset_factory(CartForm, CartItem, extra=2)
    if items:
        kwargs = {'queryset': items, }
        cart_formset = CartFormSet(data, **kwargs)
    else:
        cart_formset = CartFormSet(data)
    for form in cart_formset:
        for item in items:
            if form.instance.pk == item.pk:
                form.instance = item
    return cart_formset
