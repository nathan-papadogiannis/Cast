from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

# Create your models here.

User = get_user_model()


class NewsPost(models.Model):
    header_image = models.ImageField(upload_to='news/images')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    body = models.TextField()

    def __str__(self):
        return self.title

# class Forecast:
#     # f - JSON response from One Call
#     def __init__(self, f):
#         lat = f[]
#
# class Current:
#     # c - current from JSON response
#     def __init__(self, c):
#         self.sunrise =
