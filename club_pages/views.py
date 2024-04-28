from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event, ActivityForm, Club
from django.urls import reverse_lazy, reverse
from .forms import (CustomManagerClubCreationForm, CustomManagerClubChangeForm,
                    CustomManagerClubClubChangeForm)

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"


class EventCreateView(CreateView):
    model = Event
    template_name = "event_new.html"
    fields = "__all__"
    # success_url = reverse_lazy("home")


class EventUpdateView(UpdateView):
    model = Event
    template_name = "event_edit.html"
    fields = "__all__"


class EventDeleteView(DeleteView):
    model = Event
    template_name = "event_delete.html"
    success_url = reverse_lazy("event_list")


# Activity form
class ActivityFormListView(ListView):
    model = ActivityForm
    template_name = "activityform_list.html"


class ActivityFormDetailView(DetailView):
    model = ActivityForm
    template_name = "activityform_detail.html"


class ActivityFormCreateView(CreateView):
    model = ActivityForm
    template_name = "activityform_new.html"
    fields = "__all__"
    # success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user # added it to club
        # form.instance.role = User.Role.MANAGER
        return super().form_valid(form)

# Clubs pages :)
class ClubListView(ListView):
    model = Club
    template_name = "club_list.html"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Club.objects.filter(title__icontains=query)
        return Club.objects.all()

class ClubDetailView(DetailView):
    model = Club
    template_name = "club_detail.html"


class ClubCreateView(CreateView):
    # model = Club
    # form_class = CustomManagerClubChangeForm
    ############## Do I really need that ???????
    form_class = CustomManagerClubClubChangeForm
    template_name = "club_new.html"
    # fields = "__all__"
    
    # def form_valid(self, form):
    #   form.instance.author = self.request.user # added it to club
    #   # import ipdb; ipdb.set_trace()
    #   form.instance.firstname = Event.first_name
    #   return super().form_valid(form)


class ClubUpdateView(UpdateView):
    model = Club
    template_name = "club_edit.html"
    fields = "__all__"


class ClubDeleteView(DeleteView):
    model = Club
    template_name = "club_delete.html"
    success_url = reverse_lazy("club_list")
