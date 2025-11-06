from django.contrib import admin
from django.utils.html import format_html
from .models import Project, ProjectComment

class ProjectCommentInline(admin.TabularInline):
    model = ProjectComment
    extra = 0
    readonly_fields = ['author', 'created_at']
    can_delete = True

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_featured_image', 'is_approved', 'is_featured', 
                   'likes', 'shares', 'created_at']
    list_filter = ['is_approved', 'is_featured', 'created_at']
    list_editable = ['is_approved', 'is_featured']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'likes', 'shares']
    filter_horizontal = ['members']
    inlines = [ProjectCommentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'members')
        }),
        ('Links', {
            'fields': ('github_link', 'live_demo_link')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Status', {
            'fields': ('is_approved', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('likes', 'shares')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_projects', 'feature_projects', 'unfeature_projects']

    def display_featured_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.featured_image.url)
        return "No Image"
    display_featured_image.short_description = 'Image'

    def approve_projects(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} projects approved.')
    approve_projects.short_description = "Approve selected projects"

    def feature_projects(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} projects featured.')
    feature_projects.short_description = "Feature selected projects"

    def unfeature_projects(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} projects unfeatured.')
    unfeature_projects.short_description = "Unfeature selected projects"

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ['project', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'project']
    search_fields = ['project__title', 'author__username', 'content']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'