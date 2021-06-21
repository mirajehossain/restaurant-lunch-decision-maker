from django.urls import path

from voting.views import (
    WinnerRestaurantRetrieveAPIView,
    VotesOnItemCreateAPIView,
    MakeVotDecisionAPIView
)

app_name = 'votes'

urlpatterns = [
    path('winner-restaurant', WinnerRestaurantRetrieveAPIView.as_view(), name='v1-winner-restaurant-for-day'),
    path('votes-on-item', VotesOnItemCreateAPIView.as_view(), name='v1-votes-item'),
    path('make-vote-decision', MakeVotDecisionAPIView.as_view(), name='v1-make-vote-decision-for-today'),
]
