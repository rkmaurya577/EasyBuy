from django.contrib import admin
from .models import UserStripe, UserEmailConfirmed

# Register your models here.
admin.site.register(UserStripe)
admin.site.register(UserEmailConfirmed)