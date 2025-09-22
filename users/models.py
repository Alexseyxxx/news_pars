#до
# import uuid
# from datetime import timedelta
# from django.db import models
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils import timezone


# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Email is required")
#         email = self.normalize_email(email)

#         # если username не передан, сгенерируем его автоматически
#         if not extra_fields.get("username"):
#             extra_fields["username"] = str(uuid.uuid4())[:30]

#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=False)
#     activation_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     expired_code = models.DateTimeField(null=True, blank=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []  # пусто, чтобы createsuperuser не требовал username

#     objects = UserManager()  # подключаем кастомный менеджер

#     def save(self, *args, **kwargs):
#         if not self.pk:  
#             self.is_active = False
#             self.activation_code = uuid.uuid4()
#             self.expired_code = timezone.now() + timedelta(minutes=3)
#         super().save(*args, **kwargs)


import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expired_code = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.is_active = False
            self.activation_code = uuid.uuid4()
            self.expired_code = timezone.now() + timedelta(minutes=3)
        super().save(*args, **kwargs)
