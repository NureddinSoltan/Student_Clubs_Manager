from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event, Club
from django.urls import reverse_lazy, reverse

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
  #success_url = reverse_lazy("home")

class EventUpdateView(UpdateView):
  model = Event
  template_name = "event_edit.html"
  fields = "__all__"

class EventDeleteView(DeleteView):
  model = Event
  template_name = "event_delete.html"
  success_url = reverse_lazy("event_list")

# Clubs pages :)
class ClubListView(ListView):
  model = Club
  template_name = "club_list.html"

class ClubDetailView(DetailView):
  model = Club
  template_name = "club_detail.html"

class ClubCreateView(CreateView):
  model = Club
  template_name = "club_new.html"
  fields = "__all__"

class ClubUpdateView(UpdateView):
  model = Club
  template_name = "club_edit.html"
  fields = "__all__"

class ClubDeleteView(DeleteView):
  model = Club
  template_name = "club_delete.html"
  success_url = reverse_lazy("club_list")
