from django.shortcuts import render,HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from .models import Cart , CartItem
from products.models import Product,ProductVariation

def view_cart(request):
	try:
		the_id=request.session["cart_id"]
	except:
		the_id = None

	if the_id:
		cart=Cart.objects.get(id=the_id)
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total = float(item.product.price) * item.quantity
			new_total += line_total
		request.session["total_items"] = cart.cartitem_set.count()
		cart.total = new_total
		cart.save()
		context={"cart" : cart}
	else:
		empty_message="Your Cart is Empty, please keep shopping"
		context={"empty":True,"empty_message" : empty_message}

	template="carts/view_cart.html"
	return render(request,template,context)


def remove_from_cart(request, id):
	try:
		the_id=request.session["cart_id"]
		cart=Cart.objects.get(id=the_id)
	except:
		return HttpResponseRedirect(reverse("view_cart"))
	cartitem = CartItem.objects.get(id=id)
	# cartitem.delete()  #also delete from admin panel
	cartitem.cart = None
	cartitem.save()  # admin can see the deleted ones
	#success message
	return HttpResponseRedirect(reverse("view_cart"))



def add_to_cart(request,slug):
	request.session.set_expiry(120000)
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

	product_var = [] #product variation
	if request.method == "POST":
		qty=request.POST["qty"]
		if not int(qty)<=0 :
			for item in request.POST:
				key = item
				val = request.POST[key]
				try:
					v = ProductVariation.objects.get(product=product,category__iexact=key, title__iexact=val)
					product_var.append(v)
				except:
					pass
			cart_item=CartItem.objects.create(cart=cart, product=product)

				
			if len(product_var) > 0:
				cart_item.product_variations.add(*product_var) # * means add each item from that list
			cart_item.quantity = qty
			cart_item.save()
			#success messsage
			return HttpResponseRedirect(reverse("view_cart"))
		#error message
	return HttpResponseRedirect(reverse("view_cart"))



