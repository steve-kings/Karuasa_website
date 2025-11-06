from django.db import models

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('notes', 'Study Notes'),
        ('exam_prep', 'Exam Preparation'),
        ('reading', 'Reading Materials'),
        ('career', 'Career Resources'),
        ('internship', 'Internship Info'),
        ('professional', 'Professional Tips'),
        ('newsletter', 'Newsletter'),
        ('past_paper', 'Past Papers'),
        ('report', 'Reports'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/', blank=True)
    external_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title