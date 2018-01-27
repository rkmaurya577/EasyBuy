from django.contrib import admin
from .models import UserStripe, UserEmailConfirmed,UserAddress,EmailMarketingSignUp,UserDefaultAddress


class UserDefaultAddressAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","shipping","billing"]
	list_editable = ["shipping","billing"]
	class Meta:
		model = UserDefaultAddress

class UserAddressAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","address","shipping","billing"]
	list_editable = ["address","shipping","billing"]
	class Meta:
		model = UserAddress

admin.site.register(UserDefaultAddress , UserDefaultAddressAdmin)
admin.site.register(UserAddress , UserAddressAdmin)
# Register your models here.
admin.site.register(UserStripe)
admin.site.register(UserEmailConfirmed)


class EmailMarketingSignupAdmin(admin.ModelAdmin):
	list_display = ("__unicode__","timestamp","updated")
	class Meta:
		model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp , EmailMarketingSignupAdmin)