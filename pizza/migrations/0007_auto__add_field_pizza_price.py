# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Pizza.price'
        db.add_column('pizza_pizza', 'price',
                      self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=30, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Pizza.price'
        db.delete_column('pizza_pizza', 'price')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pizza.component': {
            'Meta': {'object_name': 'Component'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'})
        },
        'pizza.deliveryman': {
            'Meta': {'object_name': 'Deliveryman'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'})
        },
        'pizza.order': {
            'Meta': {'object_name': 'Order'},
            'address': ('django.db.models.fields.TextField', [], {'default': "u''", 'blank': 'True'}),
            'city': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'deliveryman': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pizza.Deliveryman']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pizza.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pizza.Order']", 'null': 'True', 'blank': 'True'}),
            'pizza': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pizza.Pizza']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'pizza.pizza': {
            'Meta': {'object_name': 'Pizza'},
            'components': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pizza.Component']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'})
        },
        'pizza.pizzalogentry': {
            'Meta': {'object_name': 'PizzaLogEntry'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['pizza']