from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event, ActivityForm, Club, User, EventEdit, Notification
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from datetime import timedelta
from .forms import (
    CustomManagerClubCreationForm,
    CustomManagerClubChangeForm,
    CustomManagerClubClubChangeForm,
    EventForm,
)


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Fetch the last three events sorted by date in descending order
        # TODO: by Id or by what ?
        events = Event.objects.order_by('-id')[:3]  # Replace 'date' with 'created_at' if that's more appropriate
        context['event_list'] = events
        clubs = Club.objects.order_by('-id')[:4]  # Replace 'date' with 'created_at' if that's more appropriate
        context['club_list'] = clubs

        # Check if the user is a manager and has an associated club
        if user.is_authenticated and user.role == User.Role.MANAGER:
            club = Club.objects.filter(manager=user).first()
            if club:
                context['club_id'] = club.id
        return context

class ConfMsgActivityFormPageView(TemplateView):
    template_name = "conf_msg_activityform.html"

    def get_context_data(self, **kwargs):
        context = super(ConfMsgActivityFormPageView, self).get_context_data(**kwargs)
        user = self.request.user
        club = Club.objects.filter(manager=user).first()  # Assuming the user is a manager of a club
        if club:
            context['club_id'] = club.id
        # Get the action type from the URL query parameter

        context['action_type'] = self.request.GET.get('type', 'default')

        return context


class EventListView(ListView):
    model = Event
    template_name = "event_list.html"
    paginate_by = 12

    # TODO: Filtering and connect the events with the Club category
    # def get_queryset(self, **kwargs):
    #     qs = super().get_queryset(**kwargs)
    #     qs = qs.filter(status=Event.StatusChoices.accepted)
    #     # category = self.request.GET.get('category', None)
    #     # if category and category != 'all':  # Assuming 'all' or empty is used for no filter
    #     #     qs = qs.filter(club__category=category)
    #     return qs

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        # By date
        date_filter = self.request.GET.get('date', None)
        # queryset = Event.objects.prefetch_related('club')  # Prefetch related club
        queryset = Event.objects.select_related('club')  # Changed to `select_related` is more appropriate here
        queryset = queryset.filter(status=Event.StatusChoices.accepted)

        if category and category != 'all':  # Ensure 'all' is an option to list all categories
            queryset = queryset.filter(club__category=category)
        if date_filter:
            queryset = queryset.filter(date__date=date_filter)

        # TODO: sorting by date
        # queryset = queryset.order_by('-date')

        return queryset.order_by('-date') 


    # def get_weekly_events(self):
    #     today = timezone.now().date() # + timedelta(days=1)
    #     print("hoooob" + str(today))
    #     # Find the first day of the current week (Monday)
    #     start_of_week = today - timedelta(days=today.weekday())
    #     print("start" + str(start_of_week))
    #     # Find the last day of the current week (Sunday)
    #     end_of_week = start_of_week + timedelta(days=6)
    #     print("end" + str(end_of_week))
    #     weekly_events = Event.objects.filter(date__date__range=[start_of_week, end_of_week])
    #     return weekly_events
    def get_weekly_events(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return Event.objects.filter(date__date__range=[start_of_week, end_of_week], status=Event.StatusChoices.accepted).order_by('date__date')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weekly_events'] = self.get_weekly_events()
        # only categories linked that're accepted
        accepted_club_ids = Event.objects.filter(status=Event.StatusChoices.accepted).values_list('club_id', flat=True).distinct()
        context['categories'] = Club.objects.filter(id__in=accepted_club_ids).values_list('category', flat=True).distinct()
        return context

# Filtering by week 


# class EventListView(ListView):
#     model = Event
#     template_name = "event_list.html"
#     paginate_by = 12

#     # TODO: Filtering and connect the events with the Club category
#     # def get_queryset(self, **kwargs):
#     #     qs = super().get_queryset(**kwargs)
#     #     qs = qs.filter(status=Event.StatusChoices.accepted)
#     #     # category = self.request.GET.get('category', None)
#     #     # if category and category != 'all':  # Assuming 'all' or empty is used for no filter
#     #     #     qs = qs.filter(club__category=category)
#     #     return qs

#     # def get_queryset(self):
#     #     category = self.request.GET.get('category', None)
#     #     # By date
#     #     date_filter = self.request.GET.get('date', None)
#     #     # queryset = Event.objects.prefetch_related('club')  # Prefetch related club
#     #     queryset = Event.objects.select_related('club')  # Changed to `select_related` is more appropriate here
#     #     queryset = queryset.filter(status=Event.StatusChoices.accepted)

#     #     if category and category != 'all':  # Ensure 'all' is an option to list all categories
#     #         queryset = queryset.filter(club__category=category)
#     #     if date_filter:
#     #         queryset = queryset.filter(date__date=date_filter)

#     def get_queryset(self):
#         category = self.request.GET.get('category', None)
#         date_filter = self.request.GET.get('date', None)
#         queryset = Event.objects.select_related('club').filter(status=Event.StatusChoices.accepted)

#         if category and category != 'all':
#             queryset = queryset.filter(club__category=category)
#         if date_filter:
#             year, month, day = map(int, date_filter.split('-'))
#             date_obj = timezone.datetime(year, month, day)
#             start_of_week = date_obj - timedelta(days=date_obj.weekday())
#             end_of_week = start_of_week + timedelta(days=6)
#             queryset = queryset.filter(date__range=[start_of_week, end_of_week])
        
#         queryset = queryset.order_by('date')
#         return queryset
#         # TODO: sorting by date
#         # queryset = queryset.order_by('-date')

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         events = list(self.object_list)
#         events_by_week = {}
#         for event in events:
#             week_start = event.date - timedelta(days=event.date.weekday())
#             if week_start not in events_by_week:
#                 events_by_week[week_start] = []
#             events_by_week[week_start].append(event)

#         context['events_by_week'] = events_by_week
#         accepted_club_ids = Event.objects.filter(status=Event.StatusChoices.accepted).values_list('club_id', flat=True).distinct()
#         context['categories'] = Club.objects.filter(id__in=accepted_club_ids).values_list('category', flat=True).distinct()
#         return context
    
class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object  # current event
        # Filtering the events
        events = Event.objects.order_by('-id')[:3]  # Replace 'date' with 'created_at' if that's more appropriate
        context['event_list'] = events

        event_edits = EventEdit.objects.filter(event=event, status=EventEdit.StatusChoices.accepted).order_by('-id')
        if event_edits.exists():
            event_edit = event_edits.first()  # last one
            modified_fields = {}
            for field in event_edit._meta.fields:
                field_name = field.name
                if field_name.startswith('_'):
                    continue  # Skip 
                original_value = getattr(event, field_name, None)
                new_value = getattr(event_edit, field_name, None)
                if new_value is not None and new_value != original_value:
                    modified_fields[field_name] = new_value
            context['modified_fields'] = modified_fields
        else:
            context['modified_fields'] = {}
        return context

class EventCreateView(CreateView):
    model = Event
    template_name = "event_new.html"
    fields = "__all__"

    def form_valid(self, form):
        manager = self.request.user
        club = Club.objects.filter(manager=manager).first()
        
        if club:
            form.instance.club = club
        # else:
        #     return redirect('error_url')  
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})
        # return reverse_lazy('/confmsg/activityform/?type=event')
        url = reverse('confirmation_message')  # Ensure the URL name is correctly defined in your urls.py
        return f"{url}?type=event"

    
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
    form_class = EventForm
    template_name = "event_edit.html"
    # TODO: comeplte
    # fields = ["title", "event_image", "date", "description"]

    # def post(self, request, **kwargs):
    #     current_record = self.get_object().__dict__
    #     # import ipdb; ipdb.set_trace()
    #     new_record = request.POST.copy()
    #     # new_record = {key: request.POST.get(key) for key in request.POST.keys()}

    #     # changes = {key: request.Post.get[key] for key in current_record}
    #     # for key in current_record.keys():
    #     #     print(changes)
    #     changes = {}

    #     # import ipdb;ipdb.set_trace()
    #     for key in new_record.keys():
    #         # if print(changes)
    #         if current_record.get(key) and (
    #             str(new_record[key]) != str(current_record.get(key))
    #         ):
    #             print(current_record.get(key))
    #             print(str(new_record[key]))
    #             changes[key] = new_record[key]
    #         print("in")
    #         print(changes)
    #     print("out")
    #     print(changes)

    #     Event.objects.create(**changes)

    #     # 2. Use all() function to compare the values of the corresponding keys in the two dictionaries.
    #     # 3. If the values of all the keys are equal, then the two dictionaries are equal.

    #     # import ipdb; ipdb.set_trace()
    #     # print(request.POST)
    #     return super(EventUpdateView, self).post(request, **kwargs)

    def form_valid(self, form):
        current_record = self.get_object().__dict__
        # import ipdb; ipdb.set_trace()
        new_record = form.instance.__dict__

        changes = {}
        for key in new_record.keys():
            # if print(changes)
            if current_record.get(key) and (
                str(new_record[key]) != str(current_record.get(key))
            ):
                changes[key] = new_record[key]

        changes.pop("_state", None)

        event_edit = EventEdit.objects.create(**changes)
        event_edit.event_id = current_record["id"]
        event_edit.save()
        form.instance = self.get_object()
        return super().form_valid(form)
    

    def get_success_url(self):
        # return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})
        # return reverse_lazy('/confmsg/activityform/?type=event')
        url = reverse('confirmation_message')  # Ensure the URL name is correctly defined in your urls.py
        return f"{url}?type=edit_post"


class EventDeleteView(DeleteView):
    model = Event
    template_name = "event_delete.html"
    success_url = reverse_lazy("event_list")


# Event Edit
class EditEventDetailView(DetailView):
    model = EventEdit
    template_name = "edit_event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["original_event"] = self.get_object().event
        return context


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
        # Retrieve the club associated with the current user (manager)
        manager = self.request.user
        club = Club.objects.filter(manager=manager).first()

        if club:
            form.instance.club = club
        # else:
        #     return redirect('error_url')

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the Activity Form's detail view or wherever appropriate
        # return reverse_lazy('club_detail', kwargs={'pk': self.object.pk})
        # Reverse to the club it self
        # if hasattr(self, 'object') and self.object.club:
        #     return reverse_lazy('club_detail', kwargs={'pk': self.object.club.pk})
        # else:
        #     # Redirect to a fallback URL if no club is associated or if the object was not created
        #     return reverse_lazy('home')

        # return reverse_lazy('confirmation_message')
        url = reverse('confirmation_message')  # Ensure the URL name is correctly defined in your urls.py
        return f"{url}?type=activityform"


    # def form_valid(self, form):
    #     form.instance.author = self.request.user  # added it to club
    #     # form.instance.role = User.Role.MANAGER
    #     return super().form_valid(form)


# Clubs pages :)
class ClubListView(ListView):
    model = Club
    template_name = "club_list.html"
    # Best Practice
    context_object_name = "club_list"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("search", "")
        category = self.request.GET.get("category", "")
        queryset = Club.objects.all()

        if query:
            queryset = queryset.filter(title__icontains=query)
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    #  to fetch all unique categories from the Club model and pass them to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Club.objects.values_list(
            "category", flat=True
        ).distinct()
        return context


class ClubDetailView(DetailView):
    model = Club
    template_name = "club_detail.html"

    # TODO: Get context data to view the event cards that related to that club
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.get_object()  # Get the current club based on the primary key in the URL
        # Filter events related to this club and are accepted
        events = Event.objects.filter(club=club, status=Event.StatusChoices.accepted)
        context['event_list'] = events

        user = self.request.user
        # Check if the user is a manager and the manager of this club
        if user.is_authenticated and user.role == User.Role.MANAGER and user == club.manager:
            context['user_is_manager'] = True
        else:
            context['user_is_manager'] = False
        
        return context


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
        if "form" not in context:  # Ensuring the form is instantiated
            context["form"] = self.form_class()
        form = context["form"]
        if hasattr(form.fields["manager"], "queryset"):
            context["managers"] = form.fields["manager"].queryset
        return context

    # fields = "__all__"

    # def form_valid(self, form):
    #   form.instance.author = self.request.user # added it to club
    #   # import ipdb; ipdb.set_trace()
    #   form.instance.firstname = Event.first_name
    #   return super().form_valid(form)


# class ClubUpdateView(UpdateView):
#     model = Club
#     template_name = "club_edit.html"
#     fields = "__all__"

class ClubUpdateView(UpdateView):
    model = Club
    form_class = CustomManagerClubChangeForm
    template_name = "club_edit.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:  # Ensuring the form is instantiated
            context["form"] = self.form_class(instance=self.object)
        form = context["form"]
        if hasattr(form.fields["manager"], "queryset"):
            context["managers"] = form.fields["manager"].queryset
        return context
    
    

class ClubDeleteView(DeleteView):
    model = Club
    template_name = "club_delete.html"
    success_url = reverse_lazy("club_list")


# Admin Requests
class AdminRequestTemplateView(TemplateView):
    template_name = "admin_request.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all()
        # TODO: Create new Table Same tabl as event with blank and null
        context["edit_event_post"] = EventEdit.objects.all()
        context["activity_form"] = ActivityForm.objects.all()

        # Calculate the total requests
        context["total_requests"] = (
            ActivityForm.objects.all().count()
            + Event.objects.all().count()
            + EventEdit.objects.all().count()
        )

        # Calculate status counts
        accepted_events = Event.objects.filter(
            status=Event.StatusChoices.accepted
        ).count()
        accepted_activity_form = ActivityForm.objects.filter(
            status=ActivityForm.StatusChoices.accepted
        ).count()
        accepted_events_edit = EventEdit.objects.filter(
            status=EventEdit.StatusChoices.accepted
        ).count()
        context["accepted"] = (
            accepted_events + accepted_activity_form + accepted_events_edit
        )

        rejected_events = Event.objects.filter(
            status=Event.StatusChoices.rejected
        ).count()
        rejected_activity_form = ActivityForm.objects.filter(
            status=ActivityForm.StatusChoices.rejected
        ).count()
        rejected_events_edit = EventEdit.objects.filter(
            status=EventEdit.StatusChoices.rejected
        ).count()
        context["rejected"] = (
            rejected_events + rejected_activity_form + rejected_events_edit
        )

        waiting_events = Event.objects.filter(
            status=Event.StatusChoices.waiting
        ).count()
        waiting_activity_form = ActivityForm.objects.filter(
            status=ActivityForm.StatusChoices.waiting
        ).count()
        waiting_events_edit = EventEdit.objects.filter(
            status=EventEdit.StatusChoices.waiting
        ).count()
        context["waiting"] = (
            waiting_events + waiting_activity_form + waiting_events_edit
        )

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
        request_type = self.request.GET.get("type", "")
        status_filter = self.request.GET.get("status", "")
        sort_order = self.request.GET.get("order", "new")

        # Query data based on filters
        events = (
            Event.objects.filter(status__icontains=status_filter)
            if status_filter
            else Event.objects.all()
        )
        activity_forms = (
            ActivityForm.objects.filter(status__icontains=status_filter)
            if status_filter
            else ActivityForm.objects.all()
        )
        edit_event_posts = (
            EventEdit.objects.filter(status__icontains=status_filter)
            if status_filter
            else EventEdit.objects.all()
        )

        # Filter by type if specific type is requested
        if request_type == "event":
            activity_forms = activity_forms.none()
            edit_event_posts = edit_event_posts.none()
        elif request_type == "activity":
            events = events.none()
            edit_event_posts = edit_event_posts.none()
        elif request_type == "edit":
            events = events.none()
            activity_forms = activity_forms.none()

        # # Combine and sort the results
        # all_requests = list(chain(events, activity_forms, edit_event_posts))
        # all_requests.sort(key=lambda x: x.date, reverse=(sort_order == 'new'))

        # Combine and sort the results
        all_requests = list(events) + list(activity_forms) + list(edit_event_posts)
        if sort_order == "oldest":
            all_requests.sort(key=lambda x: x.updated_at if x.updated_at else timezone.now())
        else:
            all_requests.sort(
                key=lambda x: x.updated_at if x.updated_at else timezone.now(), reverse=True
            )

        # Pass the filtered and sorted requests to the template
        context["all_requests"] = all_requests

        return context

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


class AcceptRequestView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        object = None
        if self.kwargs["request_type"] == Event.model_display():
            object = Event.objects.get(pk=self.kwargs["pk"])
            object.status = Event.StatusChoices.accepted
            # TODO: What's going on here
            self.create_notification("Creating an Event ", object, "accepted")

# Third approach
        if self.kwargs["request_type"] == EventEdit.model_display():
            # import ipdb; ipdb.set_trace()
            object = EventEdit.objects.get(pk=self.kwargs["pk"])
            populted_fields = {key: value for key, value in object.__dict__.items() if value is not None}
            # Remove keys that start with underscore (internal use)
            keys_to_remove = [key for key in populted_fields if key.startswith('_')]
            keys_to_remove.extend(["event_id", "status", "id", "updated_at"])
            for key in keys_to_remove:
                del populted_fields[key]
            object.status = EventEdit.StatusChoices.accepted
            # TODO: What's going on here
            self.create_notification("Editing an Event Post " , object.event, "accepted")
            # Assuming you meant to update the Event object associated with this EventEdit
            # if hasattr(object, 'event') and object.event:  # Not important 
            for key, value in populted_fields.items():
                setattr(object.event, key, value)
            object.event.save()

        if self.kwargs["request_type"] == ActivityForm.model_display():
            object = ActivityForm.objects.get(pk=self.kwargs["pk"])
            object.status = ActivityForm.StatusChoices.accepted
            # TODO: What's going on here
            self.create_notification("Creating an ActivityForm " ,object, "accepted")
        object.save()
        return reverse("requests")
    
    # def create_notification(self, obj, action):
    #     Notification.objects.create(
    #         recipient=obj.event.club.manager,
    #         message=f"Your request for {obj.title} has been {action}."
    #     )
    def create_notification(self, type, obj, action):
        if hasattr(obj, 'event') and obj.event.club.manager:
            recipient = obj.event.club.manager
        elif hasattr(obj, 'club') and obj.club.manager:
            recipient = obj.club.manager
        else:
            print("Error: No manager found to send notification.")
            return 

        Notification.objects.create(
            recipient=recipient,
            message=f"Your request for {type} {obj.title} has been {action}."
        )
    
# fIRST AOORIACH
        # if self.kwargs["request_type"] == EventEdit.model_display():
        #     object = EventEdit.objects.get(pk=self.kwargs["pk"])
            
        #     edited_fields = object.__dict__.copy()  # Copy the dict to avoid modifying the original object directly
        #     # filter to remove fields with None values
        #     keys_to_remove = [key for key in edited_fields if edited_fields[key] is None]
        #     for key in keys_to_remove:
        #         edited_fields.pop(key)
        #     object.status = EventEdit.StatusChoices.accepted
        #     # Assuming `event` is a related field accessible directly from `EventEdit`
        #     if hasattr(object, 'event'):
        #         object.event.objects.update(**edited_fields)


# Second APPROACH
        # if self.kwargs["request_type"] == EventEdit.model_display():
        #     object = EventEdit.objects.get(pk=self.kwargs["pk"])
        #     edited_fields = object.__dict__
        #     # filter remove null fields
        #     for key in edited_fields.keys():
        #         if edited_fields[key] == None:
        #             edited_fields.pop(key)
        #     object.status = EventEdit.StatusChoices.accepted
        #     EventEdit.event.objects.update(**edited_fields)



class RejectRequestView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        object = None
        if self.kwargs["request_type"] == Event.model_display():
            object = Event.objects.get(pk=self.kwargs["pk"])
            object.status = Event.StatusChoices.rejected
            self.create_notification("Creating an Event ", object, "rejected")

        if self.kwargs["request_type"] == EventEdit.model_display():
            object = EventEdit.objects.get(pk=self.kwargs["pk"])
            object.status = EventEdit.StatusChoices.rejected
            # TODO: What's going on here
            self.create_notification("Editing an Event Post " , object.event, "rejected")

        if self.kwargs["request_type"] == ActivityForm.model_display():
            object = ActivityForm.objects.get(pk=self.kwargs["pk"])
            object.status = ActivityForm.StatusChoices.rejected
            # TODO: What's going on here
            self.create_notification("Creating an ActivityForm " ,object, "rejected")

        object.save()
        return reverse("requests")
    
    def create_notification(self, type, obj, action):
        if hasattr(obj, 'event') and obj.event.club.manager:
            recipient = obj.event.club.manager
        elif hasattr(obj, 'club') and obj.club.manager:
            recipient = obj.club.manager
        else:
            print("Error: No manager found to send notification.")
            return  # Exit if there is no manager to notify

        Notification.objects.create(
            recipient=recipient,
            message=f"Your request for {type} {obj.title} has been {action}."
        )


from django.shortcuts import redirect
from django.views.generic import ListView
from .models import Notification

class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications.html'

    def get_queryset(self):
        # Retrieve only notifications for the logged-in user
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        # Mark all notifications as read when a specific action is performed
        Notification.objects.filter(recipient=self.request.user, read=False).update(read=True)
        return redirect('notifications')  # Adjust the redirect as necessary
    
    # Deletign all the notifications:
#     from django.http import HttpResponseRedirect

# class NotificationListView(ListView):
#     model = Notification
#     template_name = 'notifications.html'

#     def get_queryset(self):
#         # Fetch notifications and do not mark them as read yet
#         return Notification.objects.filter(recipient=self.request.user, read=False).order_by('-created_at')

#     def post(self, request, *args, **kwargs):
#         # A POST request to this view marks all notifications as read
#         Notification.objects.filter(recipient=self.request.user, read=False).update(read=True)
#         return HttpResponseRedirect(request.path_info)  # Redirect back to the same page to reflect the changes
    

    def unread_notifications_count(request):
        if request.user.is_authenticated:
            count = Notification.objects.filter(recipient=request.user, read=False).count()
            return {'unread_notifications_count': count}
        return {'unread_notifications_count': 0}

    def create_notification(self, obj, action):
        print(obj.author)
        if not obj.author:
            # Print to console for debugging purposes
            print(f"Attempted to create a notification for an object without an author: {obj}")
            return  # Exit the function to avoid creating the notification

        Notification.objects.create(
            recipient=obj.author,
            message=f"Your request for {obj.title} has been {action}."
        )