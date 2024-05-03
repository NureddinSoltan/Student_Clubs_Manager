from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event, ActivityForm, Club, User, EventEdit
from django.urls import reverse_lazy, reverse
from .forms import (CustomManagerClubCreationForm, CustomManagerClubChangeForm,
                    CustomManagerClubClubChangeForm)
from datetime import datetime
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Q
from itertools import chain

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"
    paginate_by = 12

    # TODO: Filtering and connect the events with the Club category

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(status = Event.StatusChoices.accepted)

class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"

class EventCreateView(CreateView):
    model = Event
    template_name = "event_new.html"
    fields = "__all__"
    # success_url = reverse_lazy("home")

    # def get_initial(self):
    #     # Get the initial dictionary from the superclass method

    #     initial = super(YourView, self).get_initial()

    #     # Copy the dictionary so we don't accidentally change a mutable dict
        
    #     initial = initial.copy()
    #     initial['user'] = self.request.user.pk
    #         # etc...
    #     return initial

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
    # Best Practice
    context_object_name = "club_list"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')
        queryset = Club.objects.all()

        if query:
            queryset = queryset.filter(title__icontains=query)
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    #  to fetch all unique categories from the Club model and pass them to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Club.objects.values_list('category', flat=True).distinct()
        return context

class ClubDetailView(DetailView):
    model = Club
    template_name = "club_detail.html"

class ClubCreateView(CreateView):
    # model = Club
    # form_class = CustomManagerClubChangeForm
    ############## Do I really need that ???????
    form_class = CustomManagerClubClubChangeForm
    template_name = "club_new.html"
    # TODO: form valid for assigning an author 

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['managers'] = User.objects.filter(role=User.Role.MANAGER)
    #     return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:  # Ensuring the form is instantiated
            context['form'] = self.form_class()
        form = context['form']
        if hasattr(form.fields['manager'], 'queryset'):
            context['managers'] = form.fields['manager'].queryset
        return context
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

# Admin Requests
class AdminRequestTemplateView(TemplateView):
    template_name = "admin_request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        # TODO: Create new Table Same tabl as event with blank and null
        context['edit_event_post'] = EventEdit.objects.all()
        context['activity_form'] = ActivityForm.objects.all()

        # Calculate the total requests
        context['total_requests'] = ActivityForm.objects.all().count() + Event.objects.all().count() + EventEdit.objects.all().count()
        
        # Calculate status counts
        accepted_events = Event.objects.filter(status=Event.StatusChoices.accepted).count()
        accepted_activity_form = ActivityForm.objects.filter(status=ActivityForm.StatusChoices.accepted).count()
        accepted_events_edit= EventEdit.objects.filter(status=EventEdit.StatusChoices.accepted).count()
        context['accepted'] = accepted_events + accepted_activity_form + accepted_events_edit
        
        rejected_events = Event.objects.filter(status=Event.StatusChoices.rejected).count()
        rejected_activity_form = ActivityForm.objects.filter(status=ActivityForm.StatusChoices.rejected).count()
        rejected_events_edit = EventEdit.objects.filter(status=EventEdit.StatusChoices.rejected).count()
        context['rejected'] = rejected_events + rejected_activity_form + rejected_events_edit

        waiting_events = Event.objects.filter(status=Event.StatusChoices.waiting).count()
        waiting_activity_form = ActivityForm.objects.filter(status=ActivityForm.StatusChoices.waiting).count()
        waiting_events_edit = EventEdit.objects.filter(status=EventEdit.StatusChoices.waiting).count()
        context['waiting'] = waiting_events + waiting_activity_form + waiting_events_edit

        # TODO: Filtering by date

        # Combine all the objects

        events = Event.objects.all()
        activity_forms = ActivityForm.objects.all()
        edit_event_posts = EventEdit.objects.all()

        # # Combine queries
        # all_requests = list(events) + list(activity_forms) + list(edit_event_posts)
        
        # # Sort all_requests by date (assuming 'date' field is present and not None in all models)
        # all_requests.sort(key=lambda x: x.date if x.date else timezone.now(), reverse=True)
        
        # context['all_requests'] = all_requests


        # Filtering section

        # Retrieve filter parameters from the URL
        request_type = self.request.GET.get('type', '')
        status_filter = self.request.GET.get('status', '')
        sort_order = self.request.GET.get('order', 'new')

        # Query data based on filters
        events = Event.objects.filter(status__icontains=status_filter) if status_filter else Event.objects.all()
        activity_forms = ActivityForm.objects.filter(status__icontains=status_filter) if status_filter else ActivityForm.objects.all()
        edit_event_posts = EventEdit.objects.filter(status__icontains=status_filter) if status_filter else EventEdit.objects.all()

        # Filter by type if specific type is requested
        if request_type == 'event':
            activity_forms = activity_forms.none()
            edit_event_posts = edit_event_posts.none()
        elif request_type == 'activity':
            events = events.none()
            edit_event_posts = edit_event_posts.none()
        elif request_type == 'edit':
            events = events.none()
            activity_forms = activity_forms.none()

        # # Combine and sort the results
        # all_requests = list(chain(events, activity_forms, edit_event_posts))
        # all_requests.sort(key=lambda x: x.date, reverse=(sort_order == 'new'))

        # Combine and sort the results
        all_requests = list(events) + list(activity_forms) + list(edit_event_posts)
        if sort_order == 'oldest':
            all_requests.sort(key=lambda x: x.date if x.date else timezone.now())
        else:
            all_requests.sort(key=lambda x: x.date if x.date else timezone.now(), reverse=True)

        # Pass the filtered and sorted requests to the template
        context['all_requests'] = all_requests

        return context


class AcceptEvent(UpdateView):
    model = Event
    fields = ['status']

    # # Fletring for everyone in detail.
    # def get_queryset(self):
    #     query = self.request.GET.get('search', '')
    #     category = self.request.GET.get('category', '')
    #     queryset = Club.objects.all()

    #     if query:
    #         queryset = queryset.filter(title__icontains=query)
    #     if category:
    #         queryset = queryset.filter(category__iexact=category)
    #     return queryset

    # #  to fetch all unique categories from the Club model and pass them to the template.
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Club.objects.values_list('category', flat=True).distinct()
    #     return context