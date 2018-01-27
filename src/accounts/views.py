import re
from django.shortcuts import render,HttpResponseRedirect,Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.urlresolvers import reverse
from .forms import LoginForm , RegistrationForm
from .models import UserEmailConfirmed
from carts.models import Cart
from accounts.forms import UserAddressForm

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
		# print "hello"
		
		cart = Cart.objects.all()[0]
		request.session["cart_id"] = cart.id 
		request.session["total_items"] = cart.cartitem_set.count()
		# print cart.id
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
		print "valid"
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
	print "in activation_confirmed"
	if SHA1_RE.search(activation_key):
		print "real Key"
		try:
			instance = UserEmailConfirmed.objects.get(activation_key = activation_key)
			print "instance exist"
		except UserEmailConfirmed.DoesNotExist:
			instance = None
			messages.success(request,"There was an error with your request.")

		if instance is not None and not instance.confirmed:
			print "inside if"
			instance.confirmed=True
			instance.activation_key="confirmed"
			instance.save()
			messages.success(request,"Successfully Registered, Please confirm your email. !!")
			page_message = "Confirmation Successfull"
		elif instance is not None and instance.confirmed:
			print "inside elif"
			page_message = "Already Confirmed"
			messages.success(request,"Already Confirmed. !!")
		else:
			print "inside else"
			page_message = ""

		context = {
			"page_message" : page_message,
			}
		template = "accounts/activation_complete.html"
		return render(request,template,context)
	else:
		print "http404"
		raise Http404


def address_form_view(request):
	print request.GET
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
		if redirect is not None:
			return HttpResponseRedirect(reverse(str(redirect)))
	else:
		raise Http404