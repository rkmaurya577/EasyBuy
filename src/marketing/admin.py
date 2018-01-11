from django.contrib import admin

# Register your models here.

from .models import MarketingMessage, MarketingSlider

class MarketingMessageAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","start_date","end_date","active","featured"]
	class Meta:
		model = MarketingMessage


class MarketingSliderAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","order","start_date","end_date","active","featured"]
	list_editable = ["order","start_date","end_date","active","featured"]
	class Meta:
		model = MarketingSlider

admin.site.register(MarketingMessage , MarketingMessageAdmin)
admin.site.register(MarketingSlider , MarketingSliderAdmin)
