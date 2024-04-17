from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm):
    model = User
    # fields = UserCreationForm.Meta.fields + ("age", "email",)
    fields = (
      "username",
      "first_name",
      "email",
      "role",
    )

class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = User
    # fields = UserCreationForm.Meta.fields
    fields = (
      "username",
      "email",
      "role",
    )