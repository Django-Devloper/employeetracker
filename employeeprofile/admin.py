from django.contrib import admin
from .models import (Position,EmployeeProfile,ContactDetails,AddressDetails,AccountDetail,EducationDetail,
                     DependentDetail,InsuranceInfo,Group,Team,IdentityDetail,ProficiencyCertification)

from django.urls import reverse
from django.utils.html import format_html

class ContactDetailsAdmin(admin.ModelAdmin):
    fields = [ 'contact_number', 'emergency_contact', 'personal_email']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    list_display = ['employee__employee__first_name', 'contact_number', 'emergency_contact', 'personal_email']


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

class AddressDetailAdmin(admin.ModelAdmin):
    fields = [ 'type', 'house_no', 'city','state','pin_code']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    list_display = ['type', 'house_no', 'city','state','pin_code']

class AddressDetailsInline(admin.TabularInline):
    model = AddressDetails
    extra = 1
    exclude = ['created_by','create_at']
    fields = ['type', 'house_no', 'city','state','pin_code','edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_addressdetails_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class EducationDetailAdmin(admin.ModelAdmin):
    fields=['qualification','grade','year_of_passing','year_of_enrolment','university','collage']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    list_display = ['qualification','grade','year_of_passing','year_of_enrolment','university','collage']

class EducationDetailInline(admin.TabularInline):
    model = EducationDetail
    extra = 1
    exclude = ['created_by','create_at']
    fields = ['qualification','grade','year_of_passing','year_of_enrolment','university','collage','edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_educationdetail_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class ProficiencyAdmin(admin.ModelAdmin):
    fields = ['name','since','image','grade']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    list_display = ['name','since','image','grade']

class ProficiencyCertificationInline(admin.TabularInline):
    model = ProficiencyCertification
    extra = 1
    exclude = ['created_by','create_at']
    fields = ['name','since','image','grade','edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_proficiencycertification_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class TeamAdmin(admin.ModelAdmin):
    fields=['group','team_name','member_since','is_active']
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by=request.user
        super().save_model(request, obj, form, change)
    list_display=['group','team_name','member_since','is_active']

class TeamInline(admin.TabularInline):
    model = Team
    extra = 1
    exclude = ['created_by','create_at']
    fields = ['group','team_name','member_since','is_active','edit']
    readonly_fields = ['edit']

    def edit(self,obj):
        url = reverse('admin:employeeprofile_team_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class AccountAdmin(admin.ModelAdmin):
    fields = ['account_number','account_holder_name','bank_name','ifsc_code','bank_address','cheque','customer_id']
    def save_model(self, request, obj, form, change):
        obj.created_by=request.user
        super().save_model(request, obj, form, change)
    list_display = ['account_number','account_holder_name','bank_name','ifsc_code','bank_address','cheque','customer_id']

class AccountDetailInline(admin.TabularInline):
    model = AccountDetail
    extra = 1
    exclude = ['created_by','create_at']
    fields =  ['account_number','account_holder_name','bank_name','ifsc_code','bank_address','cheque','customer_id','edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_accountdetail_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class IdentityAdmin(admin.ModelAdmin):
    fields = ['identity_name','identity_number','front_image','back_image']
    def save_model(self, request, obj, form, change):
        obj.created_by=request.user
        super().save_model(request, obj, form, change)
    list_display = ['identity_name','identity_number','front_image','back_image']

class IdentityDetailInline(admin.TabularInline):
    model = IdentityDetail
    extra = 1
    exclude = ['created_by','create_at']
    fields =['identity_name','identity_number','front_image','back_image','edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_identitydetail_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class DependentDetailAdmin(admin.ModelAdmin):
    fields = ['relationship','dependent_name','dependent_DOB']
    def save_model(self, request, obj, form, change):
        obj.created_by=request.user
        super().save_model(request, obj, form, change)
    list_display = ['relationship','dependent_name','dependent_DOB']

class DependentDetailInline(admin.TabularInline):
    model = DependentDetail
    extra = 1
    exclude = ['created_by','create_at']
    fields = ['relationship','dependent_name','dependent_DOB','edit']
    readonly_fields = ['edit']

    def edit(self, obj):
        url = reverse('admin:employeeprofile_dependentdetail_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class InsuranceAdmin(admin.ModelAdmin):
    inlines = [DependentDetailInline]
    fields = ['insurer','insured','type_of_insurance','sum_insured','policy_type','policy_number','valid_from','valid_till','documentation','card']
    def save_model(self, request, obj, form, change):
        obj.created_by=request.user
        super().save_model(request, obj, form, change)
    list_display = ['insurer','insured','type_of_insurance','sum_insured','policy_type','policy_number','valid_from','valid_till','documentation','card']

class InsuranceInfoInline(admin.TabularInline):
    model = InsuranceInfo
    extra = 1
    exclude = ['created_by','create_at']
    fields=['insurer','insured','type_of_insurance','sum_insured','policy_type','policy_number','valid_from','valid_till','documentation','card','edit']
    readonly_fields = ['edit']

    def edit(self,obj):
        url = reverse('admin:employeeprofile_insuranceinfo_change', args=[obj.pk])
        return format_html(u'<a href="{}">Edit</a>', url)

class PositionAdmin(admin.ModelAdmin):
    model = Position
    exclude = ['created_by','create_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class EmployeeProfileAdmin(admin.ModelAdmin):
    inlines = [ContactDetailsInline,AddressDetailsInline,
               EducationDetailInline,ProficiencyCertificationInline,
               TeamInline,AccountDetailInline,IdentityDetailInline,
               InsuranceInfoInline]
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

admin.site.register(EmployeeProfile,EmployeeProfileAdmin)
admin.site.register(Position,PositionAdmin)
admin.site.register(ContactDetails,ContactDetailsAdmin)
admin.site.register(AddressDetails,AddressDetailAdmin)
admin.site.register(EducationDetail,EducationDetailAdmin)
admin.site.register(ProficiencyCertification,ProficiencyAdmin)
admin.site.register(AccountDetail,AccountAdmin)
admin.site.register(InsuranceInfo,InsuranceAdmin)
admin.site.register(DependentDetail,DependentDetailAdmin)
admin.site.register(IdentityDetail,IdentityAdmin)
admin.site.register(Team,TeamAdmin)



