from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class Vote(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('active')
        INACTIVE = 'inactive', _('inactive')
        DELETED = 'deleted', _('deleted')

    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    employee = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices,
                              default=Status.ACTIVE)

    def __str__(self):
        return self.status

    class Meta:
        db_table = 'votes'


class VoteResult(BaseModel):
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    number_of_votes = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.item.name

    class Meta:
        db_table = 'vote_results'
