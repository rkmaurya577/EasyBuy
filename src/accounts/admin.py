from django.contrib import admin
from .models import UserStripe, UserEmailConfirmed
from accounts.models import EmailMarketingSignUp

# Register your models here.
admin.site.register(UserStripe)
admin.site.register(UserEmailConfirmed)

class EmailMarketingSignupAdmin(admin.ModelAdmin):
	list_display = ("__unicode__","timestamp","updated")
	class Meta:
		model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp , EmailMarketingSignupAdmin)