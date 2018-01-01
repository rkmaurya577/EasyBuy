from django.contrib import admin

# Register your models here.
from .models import Product
from .models import ProductImage,ProductVariation

class ProductAdmin(admin.ModelAdmin):
	date_hierarchy = "timestamp"
	search_fields = ["title","description"]
	list_display = ["title","price","active","updated"]
	list_editable = ["price","active"]
	list_filter = ["price","active"]
	readonly_fields = ["timestamp","updated"]
	prepopulated_fields = {"slug":("title",)} #its a dictionary
	class Meta:
		model = Product


class ProductImageAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","featured","active","updated"]
	list_editable = ["featured","active"]
	list_filter = ["featured","active"]
	class Meta:
		model = ProductImage



admin.site.register(Product , ProductAdmin)
admin.site.register(ProductImage , ProductImageAdmin)
admin.site.register(ProductVariation)