from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'registration_number', 
                   'member_type', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['member_type', 'is_verified', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'registration_number']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Member Information', {
            'fields': ('registration_number', 'member_type', 'phone_number', 
                      'course', 'year_of_study', 'profile_picture', 'is_verified',
                      'mpesa_transaction_code')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Member Information', {
            'fields': ('registration_number', 'member_type', 'phone_number', 
                      'course', 'year_of_study', 'profile_picture')
        }),
    )
    
    actions = ['verify_members', 'unverify_members']

    def verify_members(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f'{queryset.count()} members verified.')
    verify_members.short_description = "Verify selected members"

    def unverify_members(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f'{queryset.count()} members unverified.')
    unverify_members.short_description = "Unverify selected members"


    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True)
        # Also verify the members
        for transaction in queryset:
            transaction.member.is_verified = True
            transaction.member.is_active = True
            transaction.member.save()
        self.message_user(request, f'{queryset.count()} transactions marked as completed.')
    mark_completed.short_description = "Mark selected transactions as completed"

    def mark_pending(self, request, queryset):
        queryset.update(is_completed=False)
        self.message_user(request, f'{queryset.count()} transactions marked as pending.')
    mark_pending.short_description = "Mark selected transactions as pending"

admin.site.register(Member, CustomUserAdmin)