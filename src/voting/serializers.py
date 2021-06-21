from rest_framework import serializers

from user.serializers import UserLiteSerializer
from voting.models import Vote, VoteResult
from item.serializers import RestaurantSerializer, ItemLiteSerializer


class VoteSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = '__all__'

    def get_restaurant(self, obj):
        return RestaurantSerializer(obj.item.restaurant).data

    def get_item(self, obj):
        return ItemLiteSerializer(obj.item).data

    def get_employee(self, obj):
        return UserLiteSerializer(obj.employee).data


class VoteResultSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()

    class Meta:
        model = VoteResult
        fields = '__all__'

    def get_restaurant(self, obj):
        return RestaurantSerializer(obj.restaurant).data

    def get_item(self, obj):
        return ItemLiteSerializer(obj.item).data
