from django.db import models

class Event(models.Model):
    EVENT_TYPES = [
        ('upcoming', 'Upcoming Event'),
        ('past', 'Past Event'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='upcoming')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='events/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EventPhoto(models.Model):
    event = models.ForeignKey(Event, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Photo for {self.event.title}"