from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class MenuHours(BaseModel):
    """
    Holds Restaurant menu hours
    like: sunday restaurant serve to menu hour Lunch Menu(12:00 PM - 03:00 PM)

    Attributes
    ----------
    restaurant: restaurant foreign key
    name: name of the menu like "Lunch, Breakfast"
    week_day: name of the week day like "Saturday, Sunday"
    start_time: start time of the menu in 24hr format
    end_time: end time of the menu in 24hr format
    status: active, archived, delete
    """

    class Status(models.TextChoices):
        ACTIVE = 'active', _('active')
        ARCHIVED = 'archived', _('archived')
        DELETED = 'deleted', _('deleted')

    class WeekDay(models.TextChoices):
        SUNDAY = 'sunday', _('sunday')
        MONDAY = 'monday', _('monday')
        TUESDAY = 'tuesday', _('tuesday')
        WEDNESDAY = 'wednesday', _('wednesday')
        THURSDAY = 'thursday', _('thursday')
        FRIDAY = 'friday', _('friday')
        SATURDAY = 'saturday', _('saturday')

    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    week_day = models.CharField(max_length=50, choices=WeekDay.choices, default=WeekDay.SUNDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=30, choices=Status.choices,
                              default=Status.ACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Menu Hour')
        verbose_name_plural = _('Menu Hours')
        db_table = 'menu_hours'
        constraints = [
            models.UniqueConstraint(
                fields=['restaurant', 'name', 'week_day'],
                name='unique_restaurant_menu_hour_name'),
        ]

