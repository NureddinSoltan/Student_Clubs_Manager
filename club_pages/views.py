from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Event

# Create your views here.
class HomePageView(TemplateView):
  template_name = "home.html"

class EventListView(ListView):
  model = Event
  template_name = "event_list.html"


