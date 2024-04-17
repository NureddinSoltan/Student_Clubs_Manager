from django.urls import path

from .views import HomePageView, EventListView

urlpatterns = [
  path("", HomePageView.as_view(), name= "home"),
  path("events/", EventListView.as_view(), name="event_list")
]