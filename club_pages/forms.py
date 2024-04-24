from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Club, User
from django.db.models import Q
from django import forms

# I can do it without these things ??????????
class CustomManagerClubCreationForm(UserCreationForm):
  class Meta(UserCreationForm):
    model = Club
    fields = "__all__"

class CustomManagerClubChangeForm(UserChangeForm):
  class Meta:
    model = Club
    fields = "__all__"

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      
      # Filter the queryset for the manager field
      available_managers = User.objects.filter(role=User.Role.MANAGER).filter(
          Q(club=self.instance.id) | Q(club__isnull=True)
      )
      self.fields["manager"].queryset = available_managers

class CustomManagerClubClubChangeForm(forms.ModelForm):
  class Meta:
    model = Club
    fields = "__all__"

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Filter the queryset for the manager field
    available_managers = User.objects.filter(role=User.Role.MANAGER).filter(
        Q(club=self.instance.id) | Q(club__isnull=True)
    )
    self.fields["manager"].queryset = available_managers