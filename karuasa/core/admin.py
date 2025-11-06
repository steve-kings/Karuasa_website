from django.contrib import admin
from django.utils.html import format_html
from .models import SiteInfo, SliderImage, Partner, Testimonial, Leader,Constitution, ContactMessage

@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'display_logo']
    list_editable = ['email', 'phone']
    
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "No Logo"
    display_logo.short_description = 'Logo'

@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_image', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_logo', 'website', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active', 'website']
    search_fields = ['name', 'description']
    
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: contain;" />', obj.logo.url)
        return "No Logo"
    display_logo.short_description = 'Logo'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author', 'role', 'content_preview', 'is_approved', 'likes', 'created_at']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['author', 'content', 'role']
    actions = ['approve_testimonials', 'disapprove_testimonials']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} testimonials approved.')
    approve_testimonials.short_description = "Approve selected testimonials"
    
    def disapprove_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} testimonials disapproved.')
    disapprove_testimonials.short_description = "Disapprove selected testimonials"

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'display_image', 'order', 'is_active', 'email']
    list_filter = ['position', 'is_active']
    list_editable = ['order', 'is_active', 'position']
    search_fields = ['name', 'position', 'bio', 'email']
    actions = ['activate_leaders', 'deactivate_leaders']
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'
    
    def bio_preview(self, obj):
        return obj.bio[:100] + '...' if len(obj.bio) > 100 else obj.bio
    bio_preview.short_description = 'Bio Preview'
    
    def activate_leaders(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} leaders activated.')
    activate_leaders.short_description = "Activate selected leaders"
    
    def deactivate_leaders(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} leaders deactivated.')
    deactivate_leaders.short_description = "Deactivate selected leaders"
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'image', 'bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Use order to control display sequence (lower numbers show first)'
        })
    )


@admin.register(Constitution)
class ConstitutionAdmin(admin.ModelAdmin):
    list_display = ['title', 'version', 'effective_date', 'is_active']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Admin Management', {
            'fields': ('status', 'admin_notes')
        }),
    )