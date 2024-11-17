from django.contrib import admin
from llm.models import Upload_Content, Index_Name, Session

# Register your models here.
class Upload_ContentAdmin(admin.ModelAdmin):
    fields = [ 'index_name','file_name', 'file',]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ['index_name','file_name', 'file', 'chunk_size','embedding_cost','embedding_status']
    def has_change_permission(self, request, obj=None):
        return False

class Upload_contentTabluerInline(admin.TabularInline):
    model = Upload_Content
    extra = 1
    exclude = ['created_by', 'create_at']
    show_change_link = True
    fields = ['file_name', 'file','chunk_size','embedding_cost','embedding_status']
    readonly_fields = ['chunk_size','embedding_cost','embedding_status']
    def has_change_permission(self, request, obj=None):
        return False

class Index_NameAdmin(admin.ModelAdmin):
    inlines = [Upload_contentTabluerInline,]
    exclude = ['created_by', 'create_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.save()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name']
        return []

admin.site.register(Upload_Content,Upload_ContentAdmin)
admin.site.register(Index_Name,Index_NameAdmin)
admin.site.register(Session)