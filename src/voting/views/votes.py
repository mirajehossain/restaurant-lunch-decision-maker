from datetime import datetime, timedelta

from django.db.models import Count, F
from django.db.models.functions import Coalesce
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from item.models import Item
from user import permissions
from voting.serializers import (
    VoteResultSerializer,
    VoteSerializer
)
from voting.models import Vote, VoteResult


class WinnerRestaurantRetrieveAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsSuperUser | permissions.IsRestaurantOwner | permissions.IsEmployee]

    def get(self, request, *args, **kwargs):
        today_date = datetime.now()
        end_date_today = today_date
        start_date_today = end_date_today - timedelta(hours=2)
        print(start_date_today, end_date_today)
        result = VoteResult.objects.filter(date__gte=start_date_today, date__lt=end_date_today).first()

        return Response(
            {'success': True, 'data': VoteResultSerializer(result).data}, status=status.HTTP_200_OK
        )


class MakeVotDecisionAPIView(CreateAPIView):
    permission_classes = [permissions.IsSuperUser]

    def post(self, request, *args, **kwargs):
        today_date = datetime.now()
        start_date_today = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date_today = start_date_today + timedelta(1)
        result = VoteResult.objects.filter(date__gte=start_date_today, date__lt=end_date_today).first()

        if result:
            return Response(
                {'success': False, 'message': 'voting result already generated for today'},
                status=status.HTTP_400_BAD_REQUEST
            )

        maxVotes = Vote.objects \
            .filter(date__gte=start_date_today, date__lt=end_date_today) \
            .values('item_id', 'item__restaurant_id')\
            .annotate(
                item_count=Coalesce(Count(F('item_id')), 0))\
            .order_by('-item_count')\
            .values('item_id', 'item_count', 'item__restaurant_id')
        maxVotesItem = maxVotes.first()
        if len(maxVotesItem) == 0:
            return Response({
                'success': False,
                'message': 'No votes given for today'
            }, status=status.HTTP_400_BAD_REQUEST)

        lastThreeResults = VoteResult.objects.filter().order_by('-id')[:3]
        restaurantConsecutiveResult = [
            True if item.restaurant_id == maxVotesItem.get('item__restaurant_id')
            else False for item in lastThreeResults
        ]
        print(maxVotes)
        if all(restaurantConsecutiveResult) and restaurantConsecutiveResult == 3:
            voteResult = VoteResult(
                number_of_votes=maxVotes[1].get('item_count'),
                item_id=maxVotes[1].get('item_id'),
                restaurant_id=maxVotes[1].get('item__restaurant_id'),
            )
            voteResult.save()
        else:
            voteResult = VoteResult(
                number_of_votes=maxVotesItem.get('item_count'),
                item_id=maxVotesItem.get('item_id'),
                restaurant_id=maxVotesItem.get('item__restaurant_id'),
            )
            voteResult.save()
        return Response(
            {'success': True, 'data': VoteResultSerializer(voteResult).data}, status=status.HTTP_200_OK
        )


class VotesOnItemCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsEmployee]

    def post(self, request, *args, **kwargs):
        item_id = request.data.get('item_id')
        employee = self.request.user
        item = Item.objects.filter(id=item_id).first()

        if not item:
            return Response(
                {'success': False, 'message': 'item not found'}, status=status.HTTP_400_BAD_REQUEST
            )

        # check today voting is done or not
        today_date = datetime.now()
        start_date_today = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date_today = start_date_today + timedelta(1)
        result = VoteResult.objects.filter(date__gte=start_date_today, date__lt=end_date_today).first()

        if result:
            return Response(
                {'success': False, 'message': 'voting time is over for today'}, status=status.HTTP_400_BAD_REQUEST
            )

        checkEmployeeVotesForToday = Vote.objects.filter(
            date__gte=start_date_today,
            date__lt=end_date_today,
            item=item,
            employee=employee
        ).first()

        if checkEmployeeVotesForToday:
            return Response(
                {'success': False, 'message': 'You have already voted for today meal.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        vote = Vote(
            item=item,
            employee=employee
        )

        vote.save()
        return Response(
            {'success': True, 'data': VoteSerializer(vote).data}, status=status.HTTP_201_CREATED
        )
