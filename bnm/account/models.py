from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, is_staff, is_admin, usertype):
        if not email:
            raise ValueError('Email is required')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_admin=is_admin,
            usertype=usertype,
            last_login=now,
            date_joined=now,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, usertype=None):
        return self._create_user(email, username, password, False, False, usertype)

    def create_superuser(self, email, username, password):
        user = self._create_user(email, username, password, True, True, None)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERTYPE = (
        ('Company', 'Company'),
        ('Blogger', 'Blogger')
    )
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    usertype = models.CharField(max_length=254, null=True, choices=USERTYPE)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Platforms(models.Model):
    platform = models.CharField(max_length=254, null=True)

    def __str__(self):
        return self.platform


class Add_posting(models.Model):
    title = models.CharField(max_length=254, null=True)
    description = models.CharField(max_length=254, null=True)
    platforms = models.ManyToManyField(Platforms)
    advertiser = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Add_blogger_accepted(models.Model):
    add_posting = models.ForeignKey(Add_posting, null=True, on_delete=models.SET_NULL)
    accepted_blogger = models.ManyToManyField(User)