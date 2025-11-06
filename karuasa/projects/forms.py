from django import forms
from .models import Project, ProjectComment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'live_demo_link', 'featured_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'}),
        }