from django.contrib import admin
from .models import UserStripe, UserEmailConfirmed,UserAddress
from accounts.models import EmailMarketingSignUp

class UserAddressAdmin(admin.ModelAdmin):
	class Meta:
		model = UserAddress

admin.site.register(UserAddress , UserAddressAdmin)
# Register your models here.
admin.site.register(UserStripe)
admin.site.register(UserEmailConfirmed)


class EmailMarketingSignupAdmin(admin.ModelAdmin):
	list_display = ("__unicode__","timestamp","updated")
	class Meta:
		model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp , EmailMarketingSignupAdmin)