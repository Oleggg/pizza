#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Order, Deliveryman, OrderItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
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


class OrderFromCartForm(forms.ModelForm):
    city = forms.IntegerField(label = 'City', required=True )
    address = forms.CharField(label = 'Address', required=True )
    comment = forms.CharField(label = 'Comment', required=False )

    class Meta:
        model = Order
        fields = ( 'city', 'address', 'comment' )

    def save(self, *args, **kwargs):
        return super(OrderFromCartForm, self).save(*args, **kwargs)

class OrderItemForm(forms.ModelForm):
    pizza = forms.IntegerField(label = 'Pizza', required=True )
    quantity = forms.IntegerField(label = u'Количество', required=True )

    class Meta:
        model = OrderItem
        fields = ( 'pizza', 'quantity', )
    def save(self, *args, **kwargs):
        return super(OrderItemForm, self).save(*args, **kwargs)

def get_order_formset(items=None):
    #OrderItemFormset = modelformset_factory(OrderItem, form=OrderItemForm, extra=0)
    OrderItemFormset = inlineformset_factory(Order, OrderItem, extra=0)
    if items:
        kwargs = {'queryset': items, }
        #print items.values()
        #order_formset = OrderItemFormset(data, **kwargs)
        #order_formset = OrderItemFormset(**kwargs)
        order_formset = OrderItemFormset(initial = items)
        #for form, data in zip(order_formset.forms, **kwargs):
        #    form.initial = data
    else:
        order_formset = OrderItemFormset()
    for form in order_formset:
        for item in items:
            if form.instance.pk == item.pk:
                form.instance = item
    return order_formset

def get_order_from_cart_formset(items=None):

    OrderFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=0)
    order_formset = OrderFormSet()
    return order_formset
