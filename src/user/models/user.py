from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')
        OTHERS = 'others', _('others')

    class Status(models.TextChoices):
        ACTIVE = 'active', _('active')
        ARCHIVED = 'archived', _('archived')
        DELETED = 'deleted', _('deleted')

    profile_pic_url = models.TextField(null=True)
    address = models.TextField(null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    user_status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_superuser = models.BooleanField(default=False)
    password = models.TextField(null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_status', 'is_superuser']
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        default_permissions = ('add', 'change', 'view', )

    def __str__(self):
        return self.username
