from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from base.models import BaseModel


def get_default_delivery_method():
    return ['office_delivery']


class Restaurant(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('active')
        INACTIVE = 'inactive', _('inactive')
        CLOSED = 'closed', _('closed')
        SUSPENDED = 'suspended', _('suspended')
        ARCHIVED = 'archived', _('archived')

    class DeliveryMethods(models.TextChoices):
        OFFICE_DELIVERY = 'office_delivery', _('office_delivery')
        HOME_DELIVERY = 'home_delivery', _('home_delivery')
        TAKEAWAY = 'takeaway', _('takeaway')
        DINE_IN = 'dine_in', _('dine_in')

    slug = models.CharField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True)

    logo = models.TextField(null=True)
    banner = models.TextField(null=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.INACTIVE
    )
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='restaurant_owner',
    )
    is_active = models.BooleanField(default=False)
    delivery_methods = ArrayField(
        models.CharField(max_length=100, choices=DeliveryMethods.choices, default=get_default_delivery_method)
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            'name',
        ]
        db_table = 'restaurants'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
        ]
