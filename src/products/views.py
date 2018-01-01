from django.shortcuts import render,HttpResponse
from django.db.models import Q
from .models import Product , ProductImage

# Create your views here.
def home(request):
	products=Product.objects.all()
	context={
		"products" : products
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
	queryset_list=Product.objects.all()
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query) |
			Q(description__icontains=query)
			).distinct()		
	context={
			"query":query, 
		}
	template="products/search.html"
	return render(request,template,context)