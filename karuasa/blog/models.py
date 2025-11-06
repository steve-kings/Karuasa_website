from django.db import models
from members.models import Member

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    is_published = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    mentions = models.ManyToManyField(Member, related_name='mentioned_in_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"