import time

import stripe

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Create your views here.
from carts.models import Cart
from carts.models import Cart
from accounts.forms import UserAddressForm
from accounts.models import UserAddress

from .models import Order

try:
	stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
	stripe_sk= settings.STRIPE_SECRET_KEY
except Exception ,e:
	print "Exception : %s" %(e)
	NotImplementedError(str(e))

stripe.api_key = stripe_sk

def order(request):
	context={}
	template = "orders/user.html"
	return render(request, template, context)

#require user login
@login_required
def checkout(request):
	try:
		the_id=request.session["cart_id"]
		cart= Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse("view_cart"))

	try:
		new_order = Order.objects.get(cart=cart)
	except Order.DoesNotExist:
		new_order = Order()
		new_order.cart=cart
		new_order.user = request.user
		new_order.order_id = str(time.time())
		new_order.save()
	except:
		#work on some error  message
		return HttpResponseRedirect(reverse("view_cart"))
	#address added
	address_form = UserAddressForm()
	# if address_form.is_valid():
	# 	new_address = address_form.save(commit = False)
	# 	new_address.user = request.user
	# 	new_address.save()
	# print "hiiii"
	current_addresses = UserAddress.objects.filter(user=request.user)
	billing_addresses = UserAddress.objects.get_billing_addresses(user=request.user)

	if request.method == "POST":
		try:
			user_stripe = request.user.userstripe.stripe_id
			customer = stripe.Customer.retrieve(user_stripe)
		except:
			customer = None
			pass	
		if customer is not None:
			token = request.POST['stripeToken']
			print token
			card = customer.sources.create(source=token)
			charge = stripe.Charge.create(
					amount = int(new_order.final_total * 100),
					currency = "usd",
					card = card,
					customer = customer,
					description = "Charge for %s" %(request.user.username)
				)
			print card
			print charge
			if charge['captured']:
				print "charged"


	#1add shipping address
	#2add billing address
	#3run credit card
	if new_order.status == "Finished":
		del request.session["cart_id"]
		del request.session["total_items"]
		return HttpResponseRedirect(reverse("view_cart"))

	context={ 
		"order" : new_order,
		"address_form" : address_form ,
		"current_addresses" : current_addresses,
		"billing_addresses" : billing_addresses,
		"stripe_pub" : stripe_pub , 
		"stripe_sk" : stripe_sk ,
	}
	template="orders/checkout.html"
	return render(request,template,context)