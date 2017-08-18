from django.db import models

# Create your models here.
class Entry(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()

class LineUser(models.Model):
    user_id = models.CharField(max_length=64)
    display_name = models.CharField(max_length=256)
    picture_url = models.CharField(max_length=1024)
    status_message = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

