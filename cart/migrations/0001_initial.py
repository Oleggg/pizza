# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cart'
        db.create_table('cart_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('cart', ['Cart'])

        # Adding model 'CartItem'
        db.create_table('cart_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['cart.Cart'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pizza.Pizza'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('cart', ['CartItem'])


    def backwards(self, orm):
        # Deleting model 'Cart'
        db.delete_table('cart_cart')

        # Deleting model 'CartItem'
        db.delete_table('cart_cartitem')


    models = {
        'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cart.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['cart.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pizza.Pizza']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'pizza.component': {
            'Meta': {'object_name': 'Component'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'})
        },
        'pizza.pizza': {
            'Meta': {'object_name': 'Pizza'},
            'components': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pizza.Component']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'})
        }
    }

    complete_apps = ['cart']