from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventPhoto

class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1
    readonly_fields = ['display_image']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Preview'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'display_featured_image', 
                   'is_active', 'created_at']
    list_filter = ['event_type', 'is_active', 'date', 'created_at']
    list_editable = ['is_active', 'event_type']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at']
    inlines = [EventPhotoInline]
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'event_type', 'date', 'location')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def display_featured_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.featured_image.url)
        return "No Image"
    display_featured_image.short_description = 'Image'

@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ['event', 'caption', 'display_image']
    list_filter = ['event']
    search_fields = ['event__title', 'caption']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'