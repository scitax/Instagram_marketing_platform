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

    def create_superuser(self, email, password, username=None):
        user = self._create_user(email, username, password, True, True, None)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERTYPE = (
        ('Company', 'Company'),
        ('Blogger', 'Blogger')
    )
    email = models.EmailField(max_length=254, unique=True, verbose_name='Email')
    username = models.CharField(max_length=254, null=True, blank=True, verbose_name='User name')
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    usertype = models.CharField(max_length=254, null=True, choices=USERTYPE, verbose_name='User type')
    instagram_user_id = models.CharField(max_length=254, null=True, verbose_name='Instagram User ID')
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


class Platform(models.Model):
    platform = models.CharField(max_length=254, null=True)

    def __str__(self):
        return self.platform


class Advertisement_posting(models.Model):
    title = models.CharField(max_length=254, null=True)
    description = models.CharField(max_length=254, null=True)
    platform = models.ForeignKey(Platform, null=True, on_delete=models.SET_NULL)
    advertiser = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='Advertiser')
    accepted_blogger = models.ManyToManyField(User, related_name='Blogger')

    def __str__(self):
        return self.title


class Chat(models.Model):
    started = models.DateTimeField('started', editable=False, auto_now_add=True)
    users = models.ManyToManyField(User, related_name='chats')

    def __unicode__(self):
        users_str = ', '.join([user.username for user in self.users.all()])
        message_count = len(self.messages.all())
        return "{users} - {message_count} messages (started {started})".format(users=users_str,
                                                                               message_count=message_count,
                                                                               started=self.started)

    @classmethod
    def start(cls, first_user, another_user):
        chat = cls.users.add(first_user, another_user)
        chat.save()
        return chat

    def add_message(self, user_from, message):
        message = Message(chat=self, user_from=user_from, message_body=message)
        message.save()
        return message

class Message(models.Model):
    timestamp = models.DateTimeField('timestamp', editable=False, auto_now_add=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user_from = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message_body = models.TextField()

    def __unicode__(self):
        return "{user} says \"{message}\" ({timestamp})".format(user=self.user_from, message=self.message_body, timestamp=self.timestamp)

