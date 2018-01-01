from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'easybuy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^',include("products.urls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart/$',"carts.views.view_cart",name="view_cart"),
    url(r'^cart/(?P<id>\d+)/$',"carts.views.remove_from_cart",name="remove_from_cart"),
    url(r'^cart/(?P<slug>[\w-]+)/$',"carts.views.add_to_cart",name="add_to_cart"),
)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)