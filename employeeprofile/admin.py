from django.contrib import admin
from .models import Position,EmployeeProfile,ContactDetails,AddressDetails

# Register your models here.

admin.site.register(Position)
admin.site.register(EmployeeProfile)
admin.site.register(ContactDetails)
admin.site.register(AddressDetails)