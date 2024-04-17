from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Manager,Student, ManagerManager, Admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = User
  list_display = [
    "username",
    "role",
    "first_name",
    "last_name",
    "email",
    "is_staff",
  ]
  fieldsets = UserAdmin.fieldsets + ((None, {"fields":("role",)}),)
  add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields":("role",)}),)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Manager, UserAdmin)
admin.site.register(Student)
admin.site.register(Admin)