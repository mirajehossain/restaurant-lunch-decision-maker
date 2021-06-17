from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class Item(BaseModel):
    """
    Holds all Food Item of a restaurant

    Attributes
    ----------
    name: name of the item
    restaurant: restaurant foreign key
    price: price of the item
    description: description of the food item
    menu_hours: on which menu hour this item available
    status: delete flag for soft delete
    """

    class Status(models.TextChoices):
        ACTIVE = 'active', _('active')
        INACTIVE = 'inactive', _('inactive')
        DELETED = 'deleted', _('deleted')

    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    image = models.TextField(null=True, blank=True)
    price = models.FloatField()
    description = models.CharField(max_length=500, null=True, blank=True)
    menu_hours = models.ManyToManyField('item.MenuHours')
    status = models.CharField(max_length=30, choices=Status.choices,
                              default=Status.INACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'items'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
