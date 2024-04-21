from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomManagerCreationForm
from .models import User
# from .forms import CustomUserCreationForm
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

class ManagerSignUpView(CreateView):
    form_class = CustomManagerCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        form.instance.author = self.request.user # added it to club
        # import ipdb; ipdb.set_trace()
        form.instance.role = User.Role.MANAGER
        return super().form_valid(form)


# I don't know who add this?

# from django.contrib.auth.views import LoginView

# class CustomLoginView(LoginView):
#     template_name = "registration/login.html"  # Your login template path
#     success_url = reverse_lazy("home")  # Redirect to the home page after successful login

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["message"] = "Welcome to our site!"  # Customize the welcome message
#         return context