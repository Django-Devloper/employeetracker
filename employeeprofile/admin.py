from django.contrib import admin
from .models import (Position,EmployeeProfile,ContactDetails,AddressDetails,AccountDetail,EducationDetail,
                     DependentDetail,InsuranceInfo,Group,Team,IdentityDetail,ProficiencyCertification)

from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

# admin.site.register(Position)
# admin.site.register(Group)
# admin.site.register(EmployeeProfile)
# admin.site.register(AddressDetails)
# admin.site.register(AccountDetail)
# admin.site.register(EducationDetail)
# admin.site.register(DependentDetail)
# admin.site.register(InsuranceInfo)
# admin.site.register(Team)
# admin.site.register(IdentityDetail)
# admin.site.register(ProficiencyCertification)

class ContactDetailsAdmin(admin.ModelAdmin):
    fields = ['employee', 'contact_number', 'emergency_contact', 'personal_email']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    list_display = ['employee', 'contact_number', 'emergency_contact', 'personal_email']


class ContactDetailsInline(admin.TabularInline):
    model = ContactDetails
    extra = 1
    exclude = ['created_by','create_at']
    show_change_link = True
    fields = ['employee', 'contact_number', 'emergency_contact', 'personal_email', 'edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_contactdetails_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)


class AddressDetailsInline(admin.TabularInline):
    model = AddressDetails
    extra = 1
    exclude = ['created_by','create_at']

class EducationDetailInline(admin.TabularInline):
    model = EducationDetail
    extra = 1
    exclude = ['created_by','create_at']

class ProficiencyCertificationInline(admin.TabularInline):
    model = ProficiencyCertification
    extra = 1
    exclude = ['created_by','create_at']

class TeamInline(admin.TabularInline):
    model = Team
    extra = 1
    exclude = ['created_by','create_at']
class AccountDetailInline(admin.TabularInline):
    model = AccountDetail
    extra = 1
    exclude = ['created_by','create_at']

class IdentityDetailInline(admin.TabularInline):
    model = IdentityDetail
    extra = 1
    exclude = ['created_by','create_at']

class DependentDetailInline(admin.TabularInline):
    model = DependentDetail
    extra = 1
    exclude = ['created_by','create_at']

class InsuranceInfoInline(admin.TabularInline):
    model = InsuranceInfo
    extra = 1
    exclude = ['created_by','create_at']

class PositionAdmin(admin.ModelAdmin):
    model = Position
    exclude = ['created_by','create_at']

    def save_model(self, request, obj, form, change):
        print(request,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class GroupAdmin(admin.ModelAdmin):
    model = Group
    exclude = ['created_by','create_at']

    def save_model(self, request, obj, form, change):
        print(request,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class EmployeeProfileAdmin(admin.ModelAdmin):
    inlines = [ContactDetailsInline,AddressDetailsInline,
               EducationDetailInline,ProficiencyCertificationInline,
               TeamInline,AccountDetailInline,IdentityDetailInline,
               DependentDetailInline,InsuranceInfoInline]
    exclude = ['created_by','create_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit = False)
        for instance in instances:
            # if not change:
            instance.created_by = request.user
            instance.save()

admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(ContactDetails,ContactDetailsAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Group, GroupAdmin)

