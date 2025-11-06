from django import forms
from .models import BlogPost, BlogComment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'featured_image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'}),
        }