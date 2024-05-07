from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm):
    model = User
    # fields = UserCreationForm.Meta.fields + ("age", "email",)
    fields = (
      "username",
      "first_name",
      "last_name",
      "email",
      "role",
      "student_id",
      "password1",  # Default password field
      "password2",  # Confirm password field
    )

class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = User
    # fields = UserCreationForm.Meta.fields
    fields = (
      "username",
      "email",
      "role",
      "student_id",
    )

class CustomManagerCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = User
    fields = (
      "username",
      "first_name",
      "last_name",
      "email",
      "password1",  # Default password field
      "password2",  # Confirm password field
      "student_id",
    )

class CustomManagerChangeForm(UserChangeForm):
  class Meta:
    model = User
    fields = (
      "username",
      "email",
      "student_id",
    )
