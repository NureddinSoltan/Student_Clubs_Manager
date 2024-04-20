from django.urls import path

from .views import HomePageView, EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView

urlpatterns = [
  path("", HomePageView.as_view(), name= "home"),
  path("events/", EventListView.as_view(), name="event_list"),
  path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
  path("<int:pk>/edit/", EventUpdateView.as_view(), name="event_edit"),
  path("<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
  path("new/", EventCreateView.as_view(), name="event_new"),
  # path("clubs/", ClubListView.as_view(), name="club_list"),
  # path("<int:pk>/", ClubDetailView.as_view(), name="club_detail"),
  # path("<int:pk>/edit/", ClubUpdateView.as_view(), name="club_edit"),
  # path("<int:pk>/delete/", ClubDeleteView.as_view(), name="club_delete"),
  # path("new/", ClubCreateView.as_view(), name="club_new"),

]