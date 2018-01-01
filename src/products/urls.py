from django.conf.urls import patterns, url

from .views import (
	home,
	all,
	single,
	search
	)

urlpatterns = patterns('',
   url(r'^$',home,name="products_home"),
   url(r'^products/$',all,name="all_products"),
   url(r'^products/search/',search,name="product_search"),
   url(r'^products/(?P<slug>[\w-]+)/$',single,name="single_product"),
)
