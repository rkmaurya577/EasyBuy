from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
from django.template.loader import render_to_string

STATE_CHOICES = (
	('KA', 'Karnataka'), ('AP', 'Andhra Pradesh'), ('KL', 'Kerala'), ('TN', 'Tamil Nadu'), 
	('MH', 'Maharashtra'), ('UP', 'Uttar Pradesh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('RJ', 'Rajasthan'), 
	('HP', 'Himachal Pradesh'), ('JK', 'Jammu and Kashmir'), ('TG', 'Telangana'), ('AR', 'Arunachal Pradesh'), 
	('AS', 'Assam'), ('BR', 'Bihar'), ('CG', 'Chattisgarh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), 
	('MP', 'Madhya Pradesh'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), 
	('OR', 'Orissa'), ('PB', 'Punjab'), ('SK', 'Sikkim'), ('TR', 'Tripura'), ('UA', 'Uttarakhand'), 
	('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar'), ('CH', 'Chandigarh'), ('DN', 'Dadra and Nagar Haveli'), 
	('DD', 'Daman and Diu'), ('DL', 'Delhi'), ('LD', 'Lakshadweep'), ('PY', 'Pondicherry'),
	)


class UserDefaultAddress(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	shipping = models.ForeignKey("UserAddress", null=True, blank=True, related_name="user_default_shipping_address")
	billing = models.ForeignKey("UserAddress", null=True, blank=True, related_name="user_default_billing_address")

	def __unicode__(self):
		return str(self.user.username)

class UserAddressManager(models.Manager):
	def get_billing_addresses(self,user):
		return super(UserAddressManager,self).filter(billing=True).filter(user=user)

class UserAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	address = models.CharField(max_length=120)
	address2 = models.CharField(max_length=120,null=True,blank=True)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120, choices=STATE_CHOICES)
	country = models.CharField(max_length=120)
	zipcode = models.CharField(max_length=25)
	phone = models.CharField(max_length=120)
	shipping = models.BooleanField(default=True)
	billing = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True , auto_now=False)
	updated = models.DateTimeField(auto_now_add=False , auto_now=True)


	objects = UserAddressManager()

	def __unicode__(self):
		return str(self.user.username)

	def get_address(self):
		return "%s , %s , %s , %s , %s" %(self.address,self.city,self.state,self.zipcode,self.country)


class UserStripe(models.Model):
	user= models.OneToOneField(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=120, null=True, blank=True)

	def __unicode__(self):
		return str(self.stripe_id)



class UserEmailConfirmed(models.Model):
	user= models.OneToOneField(settings.AUTH_USER_MODEL)
	activation_key = models.CharField(max_length=200)  #basically a hashkey
	confirmed = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.confirmed)

	def activate_user_email(self):
		#send email here & render a string
		activation_url = "%s/%s" %(settings.SITE_URL,reverse("activation_view",args=[self.activation_key]))
		context = {
			"activation_key" : self.activation_key,
			"activation_url" : activation_url,
		}
		message =render_to_string("accounts/activation_message.txt",context)
		subject = "Activate your Email"
		print message
		self.email_user(subject,message,settings.DEFAULT_FROM_EMAIL)
		

	def email_user(self,subject,message,from_email=None, **kwargs):
		send_mail(subject,message,from_email, [self.user.email],kwargs)



class EmailMarketingSignUp(models.Model):
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True , auto_now=False)
	updated = models.DateTimeField(auto_now_add=False , auto_now=True)
	# confirmed = models.BooleanField(default=False)

	def __unicode__(self):
		return self.email;