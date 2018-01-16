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
    url(r'^checkout/$',"orders.views.checkout",name="checkout"),
    url(r'^order/$',"orders.views.order",name="order"),
    
    url(r'^ajax/dismiss_marketing_message$',"marketing.views.dismiss_marketing_message",name="dismiss_marketing_message"),
    url(r'^ajax/email_signup$',"marketing.views.email_signup",name="email_signup"),

    url(r'^account/logout/$',"accounts.views.logout_view",name="logout"),
    url(r'^account/login/$',"accounts.views.login_view",name="login"),
    url(r'^account/register/$',"accounts.views.registration_view",name="registration"),
    url(r'^account/activate/(?P<activation_key>\w+)/$',"accounts.views.activation_view",name="activation_view"),
)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)