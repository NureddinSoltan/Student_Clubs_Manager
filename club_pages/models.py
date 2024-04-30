from django.db import models
from django.urls import reverse
from django.conf import settings
from accounts.models import User
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


def validate_length(value):
    length = len(value)
    if length < 100:
        raise ValidationError(("description should be at least 100 character"))


class Event(models.Model):
    title = models.CharField(max_length=255)
    club = models.CharField(max_length=70)
    event_image = models.ImageField(upload_to="event_images", default="club-pic.jpeg", blank=True)
    date = models.DateTimeField(null=True)
    location = models.CharField(max_length=40)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    description = models.CharField(null=True, max_length=200, validators=[validate_length])
    body = RichTextField()
    rule = RichTextField(null=True)
    faq = RichTextField(null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # TODO: Remove this
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})


class ActivityForm(models.Model):
    title = models.CharField(max_length=255)
    club = models.CharField(max_length=70)
    date = models.DateTimeField(null=True)
    location = models.CharField(max_length=30)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    event_content = models.TextField()
    speakers = models.TextField()
    place = models.CharField(max_length=70)
    special_services = models.TextField()
    other_reqests = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("activityform_detail", kwargs={"pk": self.pk})


# def validate_manager_role(value):
#     if value.role != User.Role.MANAGER:
#         raise ValidationError('The selected manager must have the role set to "MANAGER".')


def validate_manager_role(value):
    try:
        user = User.objects.get(pk=value)
        if user.role != User.Role.MANAGER:
            raise ValidationError(
                'The selected manager must have the role set to "MANAGER".'
            )
    except User.DoesNotExist:
        pass  # or raise ValidationError('Invalid user selected.') depending on your validation logic


class Club(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=30)
    club_imgage = models.ImageField(
        upload_to="club_images", default="logo_club.png", blank=True
    )
    club_cover = models.ImageField(
        upload_to="club_images", default="club_cover_default.png", blank=True
    )
    vice_first_name = models.CharField(max_length=15, null=True)
    vice_last_name = models.CharField(max_length=15, null=True)
    about = RichTextField(null=True)
    purpose = RichTextField(null=True)
    # manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    manager = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, validators=[validate_manager_role]
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_clubs",
        null=True,
        # TODO: removethis 
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("club_detail", kwargs={"pk": self.pk})
