from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Club, User, Event
from django.db.models import Q
from django import forms
from django.forms import ModelForm

# I can do it without these things ??????????
class CustomManagerClubCreationForm(UserCreationForm):
  class Meta(UserCreationForm):
    model = Club
    fields = "__all__"

# TODO: I Changed it because of the probem in the updateView
# class CustomManagerClubChangeForm(UserChangeForm):
#   class Meta:
#     model = Club
#     fields = "__all__"

#     def __init__(self, *args, **kwargs):
#       super().__init__(*args, **kwargs)
      
#       # Filter the queryset for the manager field
#       available_managers = User.objects.filter(role=User.Role.MANAGER).filter(
#           Q(club=self.instance.id) | Q(club__isnull=True)
#       )
#       self.fields["manager"].queryset = available_managers
class CustomManagerClubChangeForm(forms.ModelForm): # Did that for the edit page
    class Meta:
        model = Club
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomManagerClubChangeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        # Adjust the queryset for the manager field
        if instance:  # Check if this is an update operation
            # Include the current manager of this club (if any) and any managers not currently assigned
            available_managers = User.objects.filter(
                Q(role=User.Role.MANAGER) & 
                (Q(club=instance) | Q(club__isnull=True))
            )
        else:  # For creating new clubs, all unassigned managers are available
            available_managers = User.objects.filter(role=User.Role.MANAGER, club__isnull=True)
        
        self.fields['manager'].queryset = available_managers

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

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('club','author','event', 'status')  # Specify the field to exclude
