from django.contrib import admin
from .models import Event, ActivityForm, Club, User, EventEdit
from django import forms
from django.db.models import Q
# Register your models here.

admin.site.register(Event)
admin.site.register(EventEdit)
admin.site.register(ActivityForm)
# admin.site.register(Club)
# class EventAdmin(admin.ModelAdmin):
#   fields = ('date', 'body')


# admin.site.register(Event, EventAdmin)
class ClubAdminForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # import ipdb; ipdb.set_trace()
        # Limit choices for the manager field to only users with the role set to 'MANAGER'

        # self.fields['manager'].queryset = User.objects.filter(role=User.Role.MANAGER)

        # available_managers = User.objects.filter(role=User.Role.MANAGER).exclude(~Q(club=self.instance.id))
        available_managers = User.objects.filter(role=User.Role.MANAGER).filter((Q(club=self.instance.id) | Q(club__isnull = True)))

        
        self.fields["manager"].queryset = available_managers


class ClubAdmin(admin.ModelAdmin):
    form = ClubAdminForm


admin.site.register(Club, ClubAdmin)
