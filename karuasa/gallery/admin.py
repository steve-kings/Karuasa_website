from django.contrib import admin
from django.utils.html import format_html
from .models import Album, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    readonly_fields = ['display_image']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Preview'

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_cover_image', 'photo_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    inlines = [PhotoInline]
    
    def display_cover_image(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.cover_image.url)
        return "No Image"
    display_cover_image.short_description = 'Cover'
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['album', 'caption', 'display_image', 'uploaded_at']
    list_filter = ['album', 'uploaded_at']
    search_fields = ['album__title', 'caption']
    readonly_fields = ['uploaded_at']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'