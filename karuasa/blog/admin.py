from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, BlogComment

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ['author', 'created_at']
    can_delete = True

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_featured_image', 'is_published', 
                   'is_approved', 'likes', 'shares', 'created_at']
    list_filter = ['is_published', 'is_approved', 'created_at', 'author']
    list_editable = ['is_published', 'is_approved']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'likes', 'shares']
    inlines = [BlogCommentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Status', {
            'fields': ('is_published', 'is_approved')
        }),
        ('Statistics', {
            'fields': ('likes', 'shares')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_posts', 'publish_posts', 'unpublish_posts']

    def display_featured_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover;" />', obj.featured_image.url)
        return "No Image"
    display_featured_image.short_description = 'Image'

    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} posts approved.')
    approve_posts.short_description = "Approve selected posts"

    def publish_posts(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f'{queryset.count()} posts published.')
    publish_posts.short_description = "Publish selected posts"

    def unpublish_posts(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f'{queryset.count()} posts unpublished.')
    unpublish_posts.short_description = "Unpublish selected posts"

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'post']
    search_fields = ['post__title', 'author__username', 'content']
    readonly_fields = ['created_at']
    filter_horizontal = ['mentions']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'