from django.conf import settings
from django.db import models
from decimal import Decimal

# Create your models here.
from carts.models import Cart

try:
	tax_rate = settings.DEFAULT_TAX_RATE
except Exception ,e:
	print "Exception : %s" %(e)
	NotImplementedError(str(e))

STATUS_CHOICES = (
	("Started", "Started"),
	("Abandoned", "Abandoned"),
	("Finished", "Finished"),
	)
 
class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,null=True)
	order_id = models.CharField(max_length=120, default='ABC',unique=True) #id is also exist
	cart = models.ForeignKey(Cart)
	status = models.CharField(max_length=120 , choices=STATUS_CHOICES, default="Started")
	#address
	sub_total= models.DecimalField(default=10.99,max_digits=100,decimal_places=2)
	tax_total= models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
	final_total= models.DecimalField(default=10.99,max_digits=100,decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True , auto_now=False)
	updated = models.DateTimeField(auto_now_add=False , auto_now=True)

	def __unicode__(self):
		return self.order_id

	def get_final_total(self):
		instance = Order.objects.get(id = self.id)
		two_places = Decimal(10) ** -2
		tax_rate_dec = Decimal(tax_rate)
		tax_total_dec = Decimal(instance.tax_total)
		sub_total_dec = Decimal(self.sub_total)
		final_total_dec = Decimal(sub_total_dec + tax_total_dec).quantize(two_places)
		instance.tax_total =sub_total_dec * tax_rate_dec
		instance.final_total = final_total_dec
		instance.save()
		return instance.final_total