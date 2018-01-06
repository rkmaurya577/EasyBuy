import re
from django.shortcuts import render,HttpResponseRedirect,Http404
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from .forms import LoginForm , RegistrationForm
from .models import UserEmailConfirmed

def logout_view(request):
	logout(request)
	return HttpResponseRedirect("/")


def login_view(request):
	form = LoginForm(request.POST or None)
	value = "Login"
	if form.is_valid():
		username=form.cleaned_data["username"]
		password=form.cleaned_data["password"]
		user=authenticate(username=username,password=password) #variable = parameter
		login(request,user)
		user.useremailconfirmed.activate_user_email()
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
		# new_user.first_name = "rahul"  #here we can do other work
		new_user.save()
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


def activation_confirmed(request, activation_key):
	print "in activation_confirmed"
	if SHA1_RE.search(activation_key):
		print "real Key"
		try:
			instance = UserEmailConfirmed.objects.get(activation_key = activation_key)
			print "instance exist"
		except UserEmailConfirmed.DoesNotExist:
			instance = None
			print "instance not exist"
			raise Http404

		if instance is not None and not instance.confirmed:
			print "inside if"
			instance.confirmed=True
			instance.activation_key="confirmed"
			instance.save()
			page_message = "Confirmation Successfull"
		elif instance is not None and instance.confirmed:
			print "inside elif"
			page_message = "Already Confirmed"
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
