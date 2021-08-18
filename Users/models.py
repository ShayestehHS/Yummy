from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have email")
        if not first_name:
            raise ValueError("User must have first name")
        if not last_name:
            raise ValueError("User must have last name")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(email, username, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user


class User(AbstractUser):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    uniqueCode = models.CharField(null=True, blank=True, max_length=500,
                                  verbose_name='Unique code')
    confirmEmailCode = models.IntegerField(null=True, blank=True,
                                           verbose_name='Verification code')
    isConfirmEmail = models.BooleanField(default=False, null=True, blank=True,
                                         verbose_name='Verified or not')
    userTry = models.PositiveSmallIntegerField(default=1)
    phoneNumber = models.IntegerField(null=True, blank=True)
    all_total = models.PositiveIntegerField(default=0)
    isDriver = models.BooleanField(default=False)
    isOwner = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    motorbike = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    driver_lic = models.BooleanField(default=False)
    mobile = models.BooleanField(default=False)
