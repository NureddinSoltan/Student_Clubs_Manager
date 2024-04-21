from django.urls import path
from .views import SignUpView, ManagerSignUpView
# CustomLoginView

urlpatterns = [
  path("signup/",SignUpView.as_view(),name="signup"),
  path("signup/manager/",ManagerSignUpView.as_view(),name="signup_manager"),

  # path('login/', CustomLoginView.as_view(), name='login'),
]