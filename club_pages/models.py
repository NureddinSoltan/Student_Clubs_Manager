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

def validate_manager_role(value):
    try:
        user = User.objects.get(pk=value)
        if user.role != User.Role.MANAGER:
            raise ValidationError(
                'The selected manager must have the role set to "MANAGER".'
            )
    except User.DoesNotExist:
        pass  # or raise ValidationError('Invalid user selected.') depending on your validation logic

# TODO: Problem with do it in that way :(
# class StatusChoices(models.TextChoices):
#     waiting = "WAITING", "waiting"
#     accepted = "ACCEPTED", "accepted"
#     rejected = "REJECTED", "rejected"
    

# Club Model
class Club(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=30)
    club_image = models.ImageField(
        upload_to="club_images", default="logo_club.png", blank=True
    )
    club_cover = models.ImageField(
        upload_to="club_images", default="club_cover_default.png", blank=True
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
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


# Event Model
class Event(models.Model):
    title = models.CharField(max_length=255)
    # club = models.CharField(max_length=40, null=True, blank=True)
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    event_image = models.ImageField(upload_to="event_images", default="club-pic.jpeg", blank=True)
    date = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    location = models.CharField(max_length=70)
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
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
    # add just for updating
    # updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class StatusChoices(models.TextChoices):
        # on the left: db, on the right: server
        waiting = "WAITING", "waiting"
        accepted = "ACCEPTED", "accepted"
        rejected = "REJECTED", "rejected"
    
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default = StatusChoices.waiting, null=True, blank=True)

    # Add Helper Method:
    def get_request_type_display(self):
        return Event.model_display()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})
    
    @staticmethod
    def model_display():
        return "Event Post"



# EventEdit Model
class EventEdit(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    # club = models.CharField(max_length=40, null=True, blank=True)
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    event_image = models.ImageField(upload_to="event_images", default="club-pic.jpeg", blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=200, validators=[validate_length], blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    rule = RichTextField(blank=True, null=True)
    faq = RichTextField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # TODO: Remove this
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    class StatusChoices(models.TextChoices):
        waiting = "WAITING", "waiting"
        accepted = "ACCEPTED", "accepted"
        rejected = "REJECTED", "rejected"

    # TODO: should Also this be a null and blank
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default = StatusChoices.waiting)

    # Add Helper Method:
    def get_request_type_display(self):
        return EventEdit.model_display()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})
    
    @staticmethod
    def model_display():
        return "Edit Event Post"


# ActivityForm Model
class ActivityForm(models.Model):
    title = models.CharField(max_length=255)
    # club = models.CharField(max_length=70, null=True, blank=True)
    club = models.ForeignKey(
    Club, on_delete=models.CASCADE,
    null=True,
    blank=True,
    )
    date = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    location = models.CharField(max_length=30)
    # first_name = models.CharField(max_length=15)
    # last_name = models.CharField(max_length=15)
    event_content = models.TextField()
    speakers = models.TextField()
    place = models.CharField(max_length=70)
    special_services = models.TextField()
    other_reqests = models.TextField()

    class StatusChoices(models.TextChoices):
        waiting = "WAITING", "waiting"
        accepted = "ACCEPTED", "accepted"
        rejected = "REJECTED", "rejected"
    
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default = StatusChoices.waiting, blank=True)
    
    # Add Helper Method
    def get_request_type_display(self):
        return ActivityForm.model_display()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("activityform_detail", kwargs={"pk": self.pk})

    @staticmethod
    def model_display():
        return "Activity Form"
    

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Notification for {self.recipient.username}"
    
    def __str__(self):
        return self.message
