from django.conf.urls import patterns, include, url
#from .views import CartDetailView
from cart import views
from .views import CartUpdateView

urlpatterns = patterns('',
    #url(r'^cart', views.cart),
    url(r'^$', views.cart),
    url(r'^cart/add/$', views.add_product),
    url(r'^cart/clear/', views.clear_cart),
    url('^edit/(?P<pk>[\w-]+)$' , CartUpdateView.as_view(), name='cart-edit'),
)
