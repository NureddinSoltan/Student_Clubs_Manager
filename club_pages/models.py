from django.db import models
from django.urls import reverse
from django.conf import settings
from accounts.models import User
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

# Create your models here.
class Event(models.Model):
  title = models.CharField(max_length = 255)
  club = models.CharField(max_length=70)
  event_imgage = models.ImageField(upload_to="event_images", default='aqsa_copy.jpeg', blank=True)
  date = models.DateField()
  location = models.CharField(max_length=30)
  first_name = models.CharField(max_length=15)
  last_name = models.CharField(max_length=15)
  body = RichTextField(max_length=10)
  # body = models.TextField()
  # Rule Section
  # FAQ section
  # Add pictures
  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete = models.CASCADE,
  )
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse("event_detail", kwargs={"pk": self.pk})

class Activity_Form(models.Model):
  title = models.CharField(max_length = 255)
  club = models.CharField(max_length=70)
  date = models.DateTimeField(blank=True)
  location = models.CharField(max_length=30)
  first_name = models.CharField(max_length=15)
  last_name = models.CharField(max_length=15)
  event_content = models.TextField()
  speakers = models.TextField()
  place = models.CharField(max_length=70)
  special_services = models.TextField()
  other_reqests = models.TextField()

# def validate_manager_role(value):
#     if value.role != User.Role.MANAGER:
#         raise ValidationError('The selected manager must have the role set to "MANAGER".')

def validate_manager_role(value):
    try:
        user = User.objects.get(pk=value)
        if user.role != User.Role.MANAGER:
            raise ValidationError('The selected manager must have the role set to "MANAGER".')
    except User.DoesNotExist:
        pass  # or raise ValidationError('Invalid user selected.') depending on your validation logic


class Club(models.Model):
  title = models.CharField(max_length = 255)
  category = models.CharField(max_length=30)
  club_imgage = models.ImageField(upload_to="club_images", default='club_default.jpeg', blank=True)
  club_cover = models.ImageField(upload_to="club_images", default='club_cover_default.png', blank=True)
  vice_first_name = models.CharField(max_length=15, null=True)
  vice_last_name = models.CharField(max_length=15, null=True)
  about = models.TextField(null=True)
  purpose = models.TextField(null=True)
  # manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
  manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, validators=[validate_manager_role])

  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete = models.CASCADE,
    related_name= "author_clubs",
    null = True,
  )
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse("club_detail", kwargs={"pk": self.pk})
