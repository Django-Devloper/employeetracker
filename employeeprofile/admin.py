from django.contrib import admin
from .models import (Position,EmployeeProfile,ContactDetails,AddressDetails,AccountDetail,EducationDetail,
                     DependentDetail,InsuranceInfo,Group,Team,IdentityDetail,ProficiencyCertification)

# Register your models here.

admin.site.register(Position)
admin.site.register(Group)
# admin.site.register(EmployeeProfile)
# admin.site.register(ContactDetails)
# admin.site.register(AddressDetails)
admin.site.register(AccountDetail)
admin.site.register(EducationDetail)
admin.site.register(DependentDetail)
admin.site.register(InsuranceInfo)
admin.site.register(Team)
admin.site.register(IdentityDetail)
admin.site.register(ProficiencyCertification)

class ContactDetailsInline(admin.TabularInline):
    model = ContactDetails
    extra = 1
    exclude = ['created_by','create_at']


class AddressDetailsInline(admin.TabularInline):
    model = AddressDetails
    extra = 1
    exclude = ['created_by','create_at']

class EmployeeProfileAdmin(admin.ModelAdmin):
    inlines = [ContactDetailsInline,AddressDetailsInline]
    exclude = ['created_by','create_at']

    def save_model(self, request, obj, form, change):
        print(request,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit = False)
        for instance in instances:
            if not change:
                instance.created_by = request.user
            instance.save()

admin.site.register(EmployeeProfile,EmployeeProfileAdmin)

