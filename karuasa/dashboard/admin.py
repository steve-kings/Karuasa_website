from django.contrib import admin
from .models import UserProgress, Course, Competition, CompetitionSubmission

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['member', 'completed_courses_count', 'total_points', 'current_level']
    list_filter = ['current_level']
    search_fields = ['member__username', 'member__email']
    filter_horizontal = ['completed_courses']
    readonly_fields = ['total_points']
    
    def completed_courses_count(self, obj):
        return obj.completed_courses.count()
    completed_courses_count.short_description = 'Courses Completed'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_code', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'course_code', 'description']
    readonly_fields = ['course_code']
    
    fieldsets = (
        (None, {
            'fields': ('course_code', 'name', 'description', 'content')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active', 'submission_count']
    list_filter = ['is_active', 'start_date', 'end_date']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    
    def submission_count(self, obj):
        return obj.competitionsubmission_set.count()
    submission_count.short_description = 'Submissions'

@admin.register(CompetitionSubmission)
class CompetitionSubmissionAdmin(admin.ModelAdmin):
    list_display = ['competition', 'participant', 'score', 'submitted_at']
    list_filter = ['competition', 'submitted_at']
    search_fields = ['competition__title', 'participant__username', 'solution']
    readonly_fields = ['submitted_at']
    
    actions = ['recalculate_scores']

    def recalculate_scores(self, request, queryset):
        # This would trigger the AI scoring again
        for submission in queryset:
            # You could implement a recalculation method here
            pass
        self.message_user(request, f'{queryset.count()} submissions marked for recalculation.')
    recalculate_scores.short_description = "Recalculate scores for selected submissions"