from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        if (user_name == 'ousstachdz'):
            other_fields.setdefault('is_active', True)
            other_fields.setdefault('is_staff', True)
            other_fields.setdefault('is_superuser', True)
        else:
            other_fields.setdefault('is_active', False)
            other_fields.setdefault('is_superuser', False)
            other_fields.setdefault('is_staff', False)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return


class User (AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name


class Project (models.Model):

    title = models.CharField(max_length=25)
    description = models.TextField(default='')
    link = models.TextField(default='')
    github_link = models.TextField(default='')
    video_link = models.TextField(default='')
    type = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Message (models.Model):

    full_name = models.CharField(max_length=25)
    subject = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=254)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
