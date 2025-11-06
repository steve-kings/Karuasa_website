from django.contrib import admin
from .models import ResourceCategory, Resource

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description_preview']
    search_fields = ['name', 'description']
    
    def description_preview(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_preview.short_description = 'Description'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'file', 'external_link', 
                   'is_active', 'created_at']
    list_filter = ['resource_type', 'category', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'resource_type', 'category')
        }),
        ('File/Link', {
            'fields': ('file', 'external_link'),
            'description': 'Provide either a file upload or external link'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    actions = ['activate_resources', 'deactivate_resources']

    def activate_resources(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} resources activated.')
    activate_resources.short_description = "Activate selected resources"

    def deactivate_resources(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} resources deactivated.')
    deactivate_resources.short_description = "Deactivate selected resources"