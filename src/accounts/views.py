import re

import time

from django.shortcuts import render,HttpResponseRedirect,Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.urlresolvers import reverse
from .forms import LoginForm , RegistrationForm
from .models import UserEmailConfirmed, UserDefaultAddress
from carts.models import Cart
from accounts.forms import UserAddressForm
from orders.models import Order

def logout_view(request):
	logout(request)
	messages.success(request,"<strong>Successfully logged out</strong> ,Feel free to <a href='%s' >login</a> again !!" %(reverse("login")),extra_tags = "safe")
	# messages.warning(request,"There is warning.")
	# messages.error(request,"There is Some error")
	return HttpResponseRedirect("%s" %(reverse("login")))


def login_view(request):
	form = LoginForm(request.POST or None)
	value = "Login"
	if form.is_valid():
		username=form.cleaned_data["username"]
		password=form.cleaned_data["password"]
		user=authenticate(username=username,password=password) #variable = parameter
		login(request,user)
		messages.success(request,"Successfully logged in ,Welcome Back")
		
		try:
			order = Order.objects.get(user=user , status = "Started")
			cart = order.cart
			request.session["cart_id"] = cart.id 
			request.session["total_items"] = cart.cartitem_set.count()
		except Order.DoesNotExist:
			new_cart = Cart()
			new_cart.save()
			request.session["cart_id"] = new_cart.id
			new_order = Order()
			new_order.cart=new_cart
			new_order.user = request.user
			new_order.order_id = str(time.time())
			new_order.save()
			pass

		return HttpResponseRedirect("/")
	context={
		"form" : form,
		"submit_btn" : value,
		"title" : value,
	}
	return render(request,"form.html",context)


def registration_view(request):
	form = RegistrationForm(request.POST or None)
	value="Register"
	if form.is_valid():
		new_user = form.save(commit=False)
		new_user.save()
		messages.success(request,"Successfully Registered, Please confirm your email !!")
		return HttpResponseRedirect("/")
		# new_user.first_name = "rahul"  #here we can do other work
		
		# username=form.cleaned_data["username"]
		# password=form.cleaned_data["password"]
		# user=authenticate(username=username,password=password) #variable = parameter
		# login(request,user)
	context={
		"form" : form,
		"submit_btn" : value,
		"title" : value,
	}
	return render(request,"form.html",context)


SHA1_RE = re.compile("^[a-f0-9]{40}$")


def activation_view(request, activation_key):
	if SHA1_RE.search(activation_key):
		try:
			instance = UserEmailConfirmed.objects.get(activation_key = activation_key)
		except UserEmailConfirmed.DoesNotExist:
			instance = None
			messages.success(request,"There was an error with your request.")

		if instance is not None and not instance.confirmed:
			instance.confirmed=True
			instance.activation_key="confirmed"
			instance.save()
			messages.success(request,"Successfully Registered, Please confirm your email. !!")
			page_message = "Confirmation Successfull"
		elif instance is not None and instance.confirmed:
			page_message = "Already Confirmed"
			messages.success(request,"Already Confirmed. !!")
		else:
			page_message = ""

		context = {
			"page_message" : page_message,
			}
		template = "accounts/activation_complete.html"
		return render(request,template,context)
	else:
		raise Http404


def address_form_view(request):
	try:
		redirect = request.GET.get("redirect")
	except:
		redirect = None
	if request.method == "POST":
		address_form = UserAddressForm(request.POST)
		if address_form.is_valid():
			new_address = address_form.save(commit = False)
			new_address.user = request.user
			new_address.save()
			is_default = address_form.cleaned_data["default"]
			if is_default:
				default_address ,created = UserDefaultAddress.objects.get_or_create(user=request.user)
				default_address.shipping = new_address
				default_address.save()
		if redirect is not None:
			return HttpResponseRedirect(reverse(str(redirect)))
	else:
		raise Http404