from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        MANAGER = "MANAGER", "manager"
        STUDENT = "STUDENT", "student"
    base_role = Role.ADMIN  # Assign the base role when logging

    # Adding a new field to the base table
    role = models.CharField(max_length=50, choices=Role.choices, default = base_role)
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.base_role
    #         return super().save(*args, **kwargs)


# Manager
class ManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MANAGER)


class Manager(User):
    base_role = User.Role.MANAGER
    manager = ManagerManager()

    class Meta:
        proxy = True

    def welcom(self):
        return "only for Managers"

# -----------------------------------------------------------------------------------------------------------------------
# I don't need this:

# class ManagerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     manager_id = models.IntegerField(null=True, blank=True)


# @receiver(post_save, sender=Manager)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "MANAGER":
#         ManagerProfile.objects.create(user=instance)


# Students
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    class Meta:
        proxy = True

    def welcom(self):
        return "only for student"

# -----------------------------------------------------------------------------------------------------------------------
# I don't need this one also:

# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     student_id = models.IntegerField(null=True, blank=True)

# @receiver(post_save, sender=Student)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "STUDENT":
#         StudentProfile.objects.create(user=instance)

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ADMIN)


class Admin(User):
    base_role = User.Role.ADMIN
    admin = AdminManager()

    class Meta:
        proxy = True

    def welcom(self):
        return "only for Admins"