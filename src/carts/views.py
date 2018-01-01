from django.shortcuts import render,HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from .models import Cart , CartItem
from products.models import Product

def view_cart(request):
	try:
		the_id=request.session["cart_id"]
	except:
		the_id = None

	if the_id:
		cart=Cart.objects.get(id=the_id)
		context={"cart" : cart}
	else:
		empty_message="Your Cart is Empty, please keep shopping"
		context={"empty":True,"empty_message" : empty_message}

	template="carts/view_cart.html"
	return render(request,template,context)




def update_cart(request,slug):
	request.session.set_expiry(120000)
	try:
		qty=request.GET.get('qty')
		update_qty=True
	except:
		qty=None
		update_qty=False

	notes={}

	try:
		color = request.GET.get('color')
	except:
		color=None
		notes['color']=color

	try:
		size = request.GET.get('size')
	except:
		size=None
		notes['size']=size

	try:
		the_id = request.session["cart_id"]
	except:
		new_cart = Cart()
		new_cart.save()
		request.session["cart_id"] = new_cart.id
		the_id = new_cart.id

	cart=Cart.objects.get(id=the_id)
	try:
		product=Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass

	#{"cart item object" , "true/false"}
	cart_item,created=CartItem.objects.get_or_create(cart=cart, product=product)
	if created:
		print "created"
	# if not cart_item in cart.items.all(): #if this product is not in cart than add this product(in means =)
	# 	cart.items.add(cart_item)
	# else:
	# 	cart.items.remove(cart_item)

	if qty and update_qty:
		if int(qty)<=0 :
			cart_item.delete()
		else:
			cart_item.quantity = qty
			cart_item.notes = notes
			cart_item.save()
	else:
		pass

	new_total = 0.00
	for item in cart.cartitem_set.all():
		line_total = float(item.product.price) * item.quantity
		new_total += line_total
	request.session["total_items"] = cart.cartitem_set.count()
	cart.total = new_total
	cart.save()
	return HttpResponseRedirect(reverse("view_cart"))



