from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Event(models.Model):
  title = models.CharField(max_length = 255)
  club = models.CharField(max_length=70)
  event_imgage = models.ImageField(upload_to="event_images", default='aqsa_copy.jpeg', blank=True)
  date = models.DateTimeField(blank=True)
  location = models.CharField(max_length=30)
  first_name = models.CharField(max_length=15)
  last_name = models.CharField(max_length=15)
  body = models.TextField()
  # Rule Section
  # FAQ section
  # Add pictures
  date = models.DateTimeField(auto_now_add = True)
  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete = models.CASCADE,
  )
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse("article_detail", kwargs={"pk": self.pk})
