from django.urls import path

from .views import (
    HomePageView,
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    ClubListView,
    ClubDetailView,
    ClubUpdateView,
    ClubDeleteView,
    ClubCreateView,
    ActivityFormListView,
    ActivityFormDetailView,
    ActivityFormCreateView,
    AdminRequestTemplateView,
    AcceptRequestView,
    RejectRequestView,
    EditEventDetailView,
    ConfMsgActivityFormPageView,
)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    # Event
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("events/<int:pk>/edit/", EventUpdateView.as_view(), name="event_edit"),
    path("events/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
    path("events/new/", EventCreateView.as_view(), name="event_new"),
    # EditEvent
    path(
        "editevents/<int:pk>/", EditEventDetailView.as_view(), name="editevent_detail"
    ),
    # Activity form
    path("activityform/", ActivityFormListView.as_view(), name="activityform_list"),
    path(
        "activityform/<int:pk>/",
        ActivityFormDetailView.as_view(),
        name="activityform_detail",
    ),
    path(
        "activityform/new/", ActivityFormCreateView.as_view(), name="activityform_new"
    ),
    # Clubs
    path("clubs/", ClubListView.as_view(), name="club_list"),
    path("clubs/<int:pk>/", ClubDetailView.as_view(), name="club_detail"),
    path("clubs/<int:pk>/edit/", ClubUpdateView.as_view(), name="club_edit"),
    path("clubs/<int:pk>/delete/", ClubDeleteView.as_view(), name="club_delete"),
    path("clubs/new/", ClubCreateView.as_view(), name="club_new"),
    # Requests Page
    path("requests/", AdminRequestTemplateView.as_view(), name="requests"),
    path("request/accept/<int:pk>/<str:request_type>/", AcceptRequestView.as_view(),name="accept_request",),
    path("request/reject/<int:pk>/<str:request_type>/", RejectRequestView.as_view(),name="reject_request",),

    # Confitmation messages
    path("confmsg/", ConfMsgActivityFormPageView.as_view(), name="confirmation_message"),

]
