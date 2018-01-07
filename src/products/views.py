from django.shortcuts import render,HttpResponse
from django.db.models import Q
from .models import Product , ProductImage
from marketing.models import MarketingMessage

# Create your views here.
def home(request):
	products=Product.objects.all()
	marketing_message = MarketingMessage.objects.all()[0]
	context={
		"products" : products,
		"marketing_message" : marketing_message ,
	}
	return render(request,"products/home.html",context)


def all(request):
	products=Product.objects.all()
	context={
		"products":products
	}
	template="products/all.html"
	return render(request,template,context)


def single(request,slug):
	try:
		product=Product.objects.get(slug=slug)
		# images = product.productimage.set_all()
		images=ProductImage.objects.filter(product=product)
		context={
			"product":product,
			"images" : images,
		}		
	except:
		pass
	template="products/single.html"
	return render(request,template,context)


def search(request):
	try:
		query = request.GET.get('q')
	except:
		query = None
	if query:
		products = Product.objects.filter(
			Q(title__icontains=query) |
			Q(description__icontains=query)
			)
		context = {'query' : query, 'products':products}
		template = 'products/search.html'
	else:
		context = {}
		template = 'products/home.html'
	return render(request,template,context)